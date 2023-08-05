from upswingutil.pms.oracle import NAME, get_key, validate_key
from upswingutil.db import Mongodb, Firestore
from upswingutil.schema import Token
from upswingutil.schema import Reservation
from datetime import datetime, timedelta
import requests
import logging


def _update_master_profile(orgId, record):
    mongo = Mongodb(orgId)
    record.update(record.get('profileDetails'))
    record['firstName'] = record.get('customer').get('personName')[0].get('givenName') if record.get('customer') \
        else record.get('company').get('companyName')
    record['middleName'] = record.get('customer').get('personName')[0].get('nameSuffix') if record.get('customer') \
        else ''
    record['lastName'] = record.get('customer').get('personName')[0].get('surname') if record.get('customer') else ''
    del record['links']
    del record['profileIdList']
    del record['profileDetails']
    if record.get('customer'):
        del record['customer']['personName']

    _alvie_profile_links = []
    _id = record.get('idObj').get('profile')
    mongo.get_collection(mongo.GUEST_COLLECTION).update_one(
        {
            '_id': record.get('idObj').get('profile')
        },
        {
            '$set': record,
            '$currentDate': {'updatedOn': True}
        },
        upsert=True
    )
    mongo.close_connection()


def _get_id(record):
    _id = next((x['id'] for x in record.get('reservationIdList') if x['type'] == 'Reservation'), None)
    return _id


def _get_guest_list(record):
    _guest_list = list()
    for item in record.get('reservationGuests'):
        _guest = dict()
        _guest['guestId'] = item.get('profileInfo').get('profileIdList')[0].get('id')
        _guest['primary'] = item.get('primary')
        _guest['birthDate'] = item.get('birthDate')
        _guest['arrivalTransport'] = item.get('arrivalTransport')
        _guest['departureTransport'] = item.get('departureTransport')
        _guest_list.append(_guest)
    return _guest_list


def _get_guest_info(record):
    return {
        'adults': record.get('roomStay').get('guestCounts').get('adults'),
        'children': record.get('roomStay').get('guestCounts').get('children'),
        'infants': 0,
        'childBuckets': record.get('roomStay').get('guestCounts').get('childBuckets'),
        'preRegistered': record.get('preRegistered'),
        'guest_list': _get_guest_list(record)
    }


def _get_transaction_info(transactions):
    return transactions


def _get_package_info(package):
    del package['transactionDate']
    return package


def _generate_day_to_day_entry(record):
    entry_list = list()
    room_rates = record.get('roomStay').get('roomRates')
    start_date = datetime.fromisoformat(record.get('roomStay').get('arrivalDate'))
    end_date = datetime.fromisoformat(record.get('roomStay').get('departureDate'))
    day_delta = timedelta(days=1)
    for i in range((end_date - start_date).days):
        _rates = next((x for x in room_rates if x['start'] == str((start_date + i * day_delta).date())), None)
        _activity = {
            'date': str((start_date + i * day_delta).date()),
            'day_of_stay': i + 1
        }
        if _rates:
            _activity.update(_rates)
        else:
            print('No entry on given date', ((start_date + i * day_delta).date()))
        entry_list.append(_activity)
    return entry_list


def _get_folio_information(record):
    data = {
        'folioWindows': record.get('folioWindows'),
        'folioHistory': record.get('folioHistory')
    }
    return data


def _get_geo_region(nationalID: int):
    result = 'unknown'
    try:
        mongo = Mongodb('upswing')
        region = mongo.get_collection('countries').find_one({"_id": nationalID}, {"region": 1})
        mongo.close_connection()
        result = region if region else 'unknown'
    except Exception as e:
        logging.error(f'Error getting geo region of nation {nationalID}')
        logging.error(e)
    finally:
        return result


def _get_reservation_id(idList):
    resv_dict = dict()
    for item in idList:
        value = item['id']
        _type = item['type']
        resv_dict[_type.lower()] = value
    return resv_dict


class ReservationSync:

    def __init__(self, orgId: str, g_cloud_token=None):
        self.orgId = orgId
        self.mongo = Mongodb(orgId)
        self.token: Token = get_key(self.orgId)
        self.g_cloud_token = g_cloud_token
        self._api_call_counter = 0

    def retrieve_data(self, clientId, token: Token, url, payload="") -> dict:
        headers = {
            'Content-Type': 'application/json',
            'x-hotelid': clientId,
            'x-app-key': token.appKey,
            'Authorization': f'Bearer {token.key}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self._api_call_counter += 1
        if response.status_code == 200:
            return dict(response.json())
        else:
            logging.error(f'Details status: {response.status_code}')
            logging.error(response.reason)
            return None

    def _extract_reservation_details(self, record):
        try:
            resv_id = record.get('id')
            hotel_id = record.get('hotelId')
            record['idObj'] = _get_reservation_id(record.get('reservationIdList'))
            logging.info(f"Extracting reservation {resv_id} additional details.")
            if self.token is None:
                self.token: Token = record.get('token')

            if not validate_key(self.token.validity):
                logging.info(f'Refreshing {NAME} token as it is about to expire')
                self.token = get_key(record.get('orgId'))

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/cancellationHistory'
            data = self.retrieve_data(record.get('hotelId'), self.token, _url)
            record['cancellation'] = data.get('cxlActivityLog') if data else None

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/linkedSummary'
            data = self.retrieve_data(record.get('hotelId'), self.token, _url)
            record['linkedReservation'] = data.get('linkedReservationList') if data else None

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/calls'
            data = self.retrieve_data(record.get('hotelId'), self.token, _url)
            record['callHistory'] = data.get('callHistory') if data else None

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/inventoryItems'
            data = self.retrieve_data(record.get('hotelId'), self.token, _url)
            record['inventoryItems'] = data.get('inventoryItems') if data else None

            _url = f'{self.token.hostName}/csh/v0/hotels/{hotel_id}/reservations/{resv_id}/folios?includeFolioHistory=true&fetchInstructions=Account&fetchInstructions=Payee&fetchInstructions=Totalbalance&fetchInstructions=Windowbalances&fetchInstructions=Payment&fetchInstructions=Postings&fetchInstructions=Transactioncodes&fetchInstructions=Reservation'
            data = self.retrieve_data(record.get('hotelId'), self.token, _url)
            record['folioInformation'] = data.get('reservationFolioInformation') if data else None

            _url = f'{self.token.hostName}/csh/v0/hotels/{hotel_id}/transactions?reservationList={resv_id}&idContext=OPERA&type=Reservation&includeGenerates=true&includeTransactionsWithFolioNo=true&includeTransactionsWithManualPostingOnly=true'
            data = self.retrieve_data(record.get('hotelId'), self.token, _url)
            if data:
                del data['links']
            record['transactions'] = data

            return record
        except Exception as e:
            logging.error(f'Error retrieving addition reservation details for {record.get("id")}')
            logging.error(e)

    def _extract_reservation(self, record):
        try:
            reservationId = record.get("reservation")["reservation"]
            hotelId = record.get('reservation')['hotelId']
            logging.info(f'Extracting reservation: {reservationId}')

            header = {
                'Content-Type': 'application/json',
                'x-hotelid': hotelId,
                'x-app-key': self.token.appKey,
                'Authorization': f'Bearer {self.token.key}'
            }

            url = f"{self.token.hostName}/rsv/v1/hotels/{hotelId}/reservations/{reservationId}?fetchInstructions" \
                  f"=Comments&fetchInstructions=GuestMemberships&fetchInstructions=GuestLastStay&fetchInstructions" \
                  f"=ProfileAwards&fetchInstructions=ScheduledActivities&fetchInstructions=ServiceRequests" \
                  f"&fetchInstructions=ReservationAwards&fetchInstructions=RevenuesAndBalances&fetchInstructions" \
                  f"=Tickets&fetchInstructions=GuestComments&fetchInstructions=Packages&fetchInstructions" \
                  f"=InventoryItems&fetchInstructions=ReservationPaymentMethods&fetchInstructions=RoutingInstructions" \
                  f"&fetchInstructions=Preferences&fetchInstructions=Memberships&fetchInstructions=Alerts" \
                  f"&fetchInstructions=Traces&fetchInstructions=ConfirmationLetters&fetchInstructions=CallHistory" \
                  f"&fetchInstructions=FixedCharges&fetchInstructions=GuestMessages&fetchInstructions" \
                  f"=ReservationPolicies&fetchInstructions=Indicators&fetchInstructions=LinkedReservations" \
                  f"&fetchInstructions=ECoupons&fetchInstructions=TrackItItems&fetchInstructions=WebRegistrationCards" \
                  f"&fetchInstructions=ServiceRequests&fetchInstructions=ReservationActivities&fetchInstructions" \
                  f"=PrepaidCards&fetchInstructions=Shares&fetchInstructions=Attachments&fetchInstructions=Locators" \
                  f"&fetchInstructions=TransactionDiversions&fetchInstructions=ECertificates&fetchInstructions" \
                  f"=UpsellInfo&fetchInstructions=RoomAssignedByAI&fetchInstructions=Reservation"
            response = requests.request("GET", url, headers=header)
            self._api_call_counter += 1
            if response.status_code == 200:
                response_json = dict(response.json()).get('reservations').get('reservation')
                if len(response_json) > 0:
                    result = response_json[0]
                    result['id'] = reservationId
                    result['token'] = self.token
                    result['orgId'] = record.get('orgId')
                    result['agent'] = record.get('agent')
                    return result
                else:
                    logging.error(f"{NAME} returned reservation {reservationId} of length zero")
            else:
                logging.error(f"{NAME} returned status code {response.status_code} for reservation {reservationId} ")
        except Exception as err:
            logging.error(f'{record} load failed due to {err}')

    def _transform_reservation(self, record):
        reservation = Reservation(
            id=record.get('id'),
            idObj=record.get('idObj'),
            orgId=record.get('orgId'),
            agent=record.get('agent'),
            token=record.get('token'),
            hotelId=record.get('hotelId'),
            globalId=f"{record.get('agent')}-{record.get('orgId')}-{record.get('hotelId')}-{record.get('id')}",
            hotelName=record.get('folioInformation').get('reservationInfo').get('hotelName'),
            arrivalDate=record.get('roomStay').get('arrivalDate'),
            departureDate=record.get('roomStay').get('departureDate'),
            expectedTimes={
                'arrival': record.get('roomStay').get('expectedTimes').get('reservationExpectedArrivalTime'),
                'departure': record.get('roomStay').get('expectedTimes').get('reservationExpectedDepartureTime')
            },
            originalTimeSpan=record.get('roomStay').get('originalTimeSpan'),
            status=record.get('reservationStatus'),
            alerts=record.get('alerts'),
            metaInfo={
                'allowAutoCheckin': record.get('allowAutoCheckin'),
                'allowMobileCheckout': record.get('allowMobileCheckout'),
                'allowMobileViewFolio': record.get('allowMobileViewFolio'),
                'allowPreRegistration': record.get('allowPreRegistration'),
                'allowedActions': record.get('allowedActions'),
                'computedReservationStatus': record.get('computedReservationStatus'),
                'creatorId': record.get('creatorId'),
                'postStayChargeAllowed': record.get('folioInformation').get('postStayChargeAllowed'),
                'preStayChargeAllowed': record.get('folioInformation').get('preStayChargeAllowed'),
                'autoCheckInAllowed': record.get('folioInformation').get('autoCheckInAllowed'),
                'postToNoShowCancelAllowed': record.get('folioInformation').get('postToNoShowCancelAllowed'),
                'stampDutyExists': record.get('folioInformation').get('stampDutyExists'),
                'roomAndTaxPosted': record.get('folioInformation').get('roomAndTaxPosted'),
                'hasOpenFolio': record.get('hasOpenFolio'),
                'lastModifierId': record.get('lastModifierId'),
                'optedForCommunication': record.get('optedForCommunication'),
                'walkIn': record.get('walkIn'),
                'printRate': record.get('printRate'),
                'remoteCheckInAllowed': record.get('roomStay').get('remoteCheckInAllowed'),
                'roomNumberLocked': record.get('roomStay').get('roomNumberLocked'),
                'roomStayReservation': record.get('roomStayReservation'),
                'reservationIndicators': record.get('reservationIndicators'),
                'routingInstructions': record.get('routingInstructions')
            },
            createBusinessDate=record.get('createBusinessDate'),
            createDateTime=record.get('createDateTime'),
            guestLocators=record.get('guestLocators'),
            lastModifyDateTime=record.get('lastModifyDateTime'),
            bookingInfo={
                'upgradeEligible': record.get('upgradeEligible'),
                'bookingMedium': record.get('roomStay').get('bookingMedium'),
                'bookingMediumDescription': record.get('roomStay').get('bookingMediumDescription'),
                'guarantee': record.get('roomStay').get('guarantee'),
                'sourceOfSaleType': record.get('sourceOfSale').get('sourceType'),
                'sourceOfSaleCode': record.get('sourceOfSale').get('sourceCode'),
            },
            financeInfo={
                'totalPoints': record.get('roomStay').get('totalPoints'),
                'totalSpending': record.get('roomStay').get('total'),
                'paymentMethod': record.get('reservationPaymentMethods'),
                'revenueBucketsInfo': record.get('revenueBucketsInfo'),
                'transactions': _get_transaction_info(record.get('transactions')),
                'revenue': record.get('cashiering')
            },
            daily_activity=_generate_day_to_day_entry(record),
            linkedReservation=record.get('linkedReservation'),
            guestInfo=_get_guest_info(record),
            eCertificates=record.get('eCertificates'),

        )
        if record.get('callHistory'):
            reservation.callHistory = record.get('callHistory')

        if record.get('cancellation'):
            reservation.cancellation = record.get('cancellation')

        if record.get('comments'):
            reservation.comments = record.get('comments')

        if record.get('reservationPolicies'):
            reservation.policies = record.get('reservationPolicies')

        if record.get('inventoryItems'):
            reservation.inventoryItems = record.get('inventoryItems')

        if record.get('preferenceCollection'):
            reservation.preferences = record.get('preferenceCollection')

        if record.get('reservationMemberships'):
            reservation.memberships = record.get('reservationMemberships')

        if record.get('reservationPackages'):
            reservation.packages = record.get('reservationPackages')

        if record.get('folioInformation'):
            _f_info = record.get('folioInformation')
            reservation.folioInformation = _get_folio_information(_f_info)
            reservation.roomStay = _f_info.get('reservationInfo').get('roomStay')
            reservation.financeInfo['taxType'] = _f_info.get('reservationInfo').get('taxType')
            reservation.financeInfo['commissionPayoutTo'] = _f_info.get('reservationInfo').get('commissionPayoutTo'),
            del _f_info

        return reservation

    def _transform_guest(self, record):
        try:
            record: Reservation = record
            if self.token is None:
                self.token: Token = record.token

            if not validate_key(self.token.validity):
                logging.info(f'Refreshing {NAME} token as it is about to expire')
                self.token = get_key(record.orgId)

            logging.info(f'Transforming guests of reservation {record.id}')
            _new_guest_list = list()
            for guest in record.guestInfo.get('guest_list'):
                _url = f'{self.token.hostName}/crm/v1/profiles/{guest.get("guestId")}?fetchInstructions=Address' \
                       f'&fetchInstructions=Comment&fetchInstructions=Communication&fetchInstructions=Correspondence' \
                       f'&fetchInstructions=DeliveryMethods&fetchInstructions=FutureReservation' \
                       f'&fetchInstructions=GdsNegotiatedRate&fetchInstructions=HistoryReservation' \
                       f'&fetchInstructions=Indicators&fetchInstructions=Keyword&fetchInstructions=Membership' \
                       f'&fetchInstructions=NegotiatedRate&fetchInstructions=Preference&fetchInstructions=Profile' \
                       f'&fetchInstructions=Relationship&fetchInstructions=SalesInfo&fetchInstructions=Subscriptions' \
                       f'&fetchInstructions=WebUserAccount'
                _profile_data = self.retrieve_data(record.hotelId, self.token, _url)
                _micro_profile = dict()
                if _profile_data:
                    idObj = dict()
                    for item in _profile_data['profileIdList']:
                        idObj[item.get('type').lower()] = item['id']
                    _profile_data['idObj'] = idObj
                    _profile_data['birthDate'] = guest.get('birthDate')
                    _update_master_profile(record.orgId, _profile_data)
                    _micro_profile['idObj'] = idObj

                _micro_profile['primary'] = guest.get('primary')
                _micro_profile['arrivalTransport'] = guest.get('arrivalTransport')
                _micro_profile['departureTransport'] = guest.get('departureTransport')
                _new_guest_list.append(_micro_profile)
                record.guestInfo['guest_list'] = _new_guest_list

                # if _micro_profile.get('primary'):
                #     _url = f'{record.token.hostName}/crm/v0/profileStatistics?profileId={guest.get("guestId")}' \
                #            f'&hotelIds={record.hotelId}&reportType=Reservation&stayFrom={record.arrivalDate}' \
                #            f'&stayTo={record.departureDate}&summary=false'
                #     _profile_statistic = retrieve_data(record.hotelId, self.token, _url).get('profileStatistic')
                #     _statistics = _profile_statistic.get('stayStatisticsDetailList')
                #     _revenue = next((x['revenue'] for x in _statistics if record.id == _get_id(x['stayDetail'])), {})
                #     record.financeInfo['revenue'] = _revenue

            del _new_guest_list
            return record
        except Exception as e:
            logging.error(f'Error while transforming guest for reservation {record.id}')
            logging.error(e)

    def _load_to_mongodb(self, record):
        try:
            logging.info(f'Adding reservation {record.id} to db {record.orgId}')
            self.mongo.get_collection(self.mongo.RESERVATION_COLLECTION).update_one({'_id': record.id},
                                                                          {'$set': record.dict(exclude={'token', 'id'})}, upsert=True)
        except Exception as e:
            logging.error(f'Error storing to respective {record.id} to db {record.orgId}')
            logging.error(e)

    def _load_to_alvie(self, record):
        firestore_db = Firestore(app='alvie')
        guest_list = [item["idObj"] for item in record.guestInfo.get('guest_list')]
        user_email_list = []
        resv_info = {
            "_id": record.id,
            "agent": record.agent,
            "orgId": record.orgId,
            "areaId": record.roomStay,
            "arrivalDate": record.arrivalDate,
            "departureDate": record.departureDate,
            "propertyId": record.hotelId,
            "propertyName": record.hotelName,
            "status": record.status,
            "travelAgentId": record.bookingInfo.get('sourceOfSaleCode'),
            "travelAgentName": record.bookingInfo.get('sourceOfSaleType')
        }
        logging.debug(f"Final reservation id : {record.id}")
        for email in user_email_list:
            docs = firestore_db.get_collection('users').where("email", "==", email).stream()
            for doc in docs:
                logging.info("loading reservation to alvie")
                firestore_db.get_collection(f'users/{doc.id}/reservations') \
                    .document(str(record.id)) \
                    .set(resv_info, merge=True)
                logging.debug(f"added to {doc.id}")

    def process(self, reservationId, hotelId):
        record = {
            'orgId': self.orgId,
            'agent': NAME,
            'reservation': {
                'reservation': reservationId,
                'hotelId': hotelId
            }
        }

        if not validate_key(self.token.validity):
            logging.info(f'Refreshing {NAME} token as it is about to expire')
            self.token = get_key(self.orgId)

        record = self._extract_reservation(record)
        record = self._extract_reservation_details(record)
        record = self._transform_reservation(record)
        record = self._transform_guest(record)
        self._load_to_mongodb(record)
        self._load_to_alvie(record)

    def __del__(self):
        logging.info(f'API calls made: {self._api_call_counter}')
        if self.mongo:
            self.mongo.close_connection()


# if __name__ == '__main__':
#     ul.G_CLOUD_PROJECT = 'aura-staging-31cae'
#     ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
#     ul.FIREBASE = '/Users/harsh/upswing/github/agent-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-' \
#                   '7c135838e9.json'
#     ul.MONGO_URI = "mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSo" \
#                    "urce=admin&readPreference=primary&appname=Agent%20RMS%20Dev&ssl=false"
#     import firebase_admin
#     cred = firebase_admin.credentials.Certificate(ul.FIREBASE)
#     firebase = firebase_admin.initialize_app(cred)
#     resv = ReservationSync('11249')
#     resv.process(23560)
#     resv.process(23590)
