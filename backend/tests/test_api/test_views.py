import re

import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnDict

from apps.cars import models as cars_models
from apps.base import models as base_models
from apps.account import models as account_models


from tests.test_api.base import BaseTestAPIClass


###################################
#    TEST's CarBrandAPIViewSet    #
###################################

@pytest.mark.django_db
class TestCarBrandAPIViewSet(BaseTestAPIClass):

    client = APIClient()
    base_path_name = 'brand'


    #------------------------ LIST ------------------------#

    def test_list_brands_by_anonymous_user(self):
        """Тест: отправка list-запроса на brand от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_brands_by_driver(self, brands, driver):
        """Тест: отправка list-запроса на brand от водителя (role='d')"""

        self._test_list__by_UN_privileged_user(driver, self.base_path_name)

    def test_list_brands_by_manager(self, brands, manager):
        """Тест: отправка list-запроса на brand от менеджера (role='m')"""

        self._test_list__by_privileged_user(manager, self.base_path_name, brands)

    # ------------------------ RETRIEVE ------------------------#
    def test_retrieve_brand_with_valid_url_kwargs_by_anonymous_user(self, brands, manager):
        """Тест: отправка retrieve-запроса на brand с valid_url_kwargs от анонимного пользователя"""

        valid_url_kwargs = {'title': 'TOYOTA'}
        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, valid_url_kwargs)

    def test_retrieve_brand_with_valid_url_kwargs_by_driver(self, brands, driver):
        """Тест: отправка retrieve-запроса на brand с valid_url_kwargs от водителя (role='d')"""

        valid_url_kwargs = {'title': 'TOYOTA'}

        self._test_retrieve__with_valid_url_kwarg_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwarg=valid_url_kwargs
        )

    def test_retrieve_brand_with_valid_url_kwarg_by_manager(self, brands, manager):
        """Тест: отправка retrieve-запроса на brand с valid_url_kwarg от менеджера (role='m')"""

        valid_url_kwarg = {'title': 'TOYOTA'}
        instance = brands.get(title=valid_url_kwarg['title'])

        self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwarg=valid_url_kwarg,
            instance=instance,
            fields=['title']
        )

    def test_retrieve_brand_with_IN_valid_pk_by_manager(self, brands, manager):
        """Тест: отправка retrieve-запроса на brand с in_valid_pk от менеджера (role='m')"""

        invalid_kwargs = {'title': 'not_brand'}

        self._test_retrieve__with_IN_invalid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            invalid_url_kwargs=invalid_kwargs
        )

    # ------------------------ CREATE ------------------------#

    def test_create_brand_with_valid_data_by_by_anonymous_user(self, brands):
        """Тест: отправка create-запроса на brand с valid_data от анонимного пользователя"""

        valid_data = dict(title='NEW BRAND')

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name,valid_data)

    def test_create_brand_with_valid_data_by_by_UN_privileged_user(self, brands, driver):
        """Тест: отправка create-запроса на brand с valid_data от водителя (role='d')"""

        valid_data = dict(title='NEW BRAND')

        self._test_create__with_valid_data_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_data=valid_data
        )

    def test_create_brand_with_valid_data_by_manager(self, manager, brands):
        """Тест: отправка create-запроса на brand с valid_data от менеджера (role='m')"""

        valid_data = dict(title='NEW BRAND')

        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=cars_models.CarBrand,
            start_count=len(brands)
        )

    def test_create_brand_with_IN_valid_data_by_manager(self, manager, brands):
        """Тест: отправка create-запроса на brand с in_valid_data от менеджера (role='m')"""

        in_valid_data = dict(not_title='NEW BRAND')

        self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                    base_path_name=self.base_path_name,
                                                                    in_valid_payload=in_valid_data,
                                                                    model=cars_models.CarBrand, start_count=len(brands))

    # ------------------------ UPDATE ------------------------#

    def test_update_brand_with_valid_data_by_anonymous_user(self, brands):
        """Тест: отправка update-запроса на brand с valid_data от анонимного пользователя"""

        valid_data = dict(title='CHANGED TITLE')
        kwargs = {
            'title': brands.first().title
        }

        self._test_update__with_valid_payload_by_anonymous_user(
            self.base_path_name, kwargs, valid_data)

    def test_update_brand_with_valid_data_by_UN_privileged_user(self, brands, driver):
        """Тест: отправка update-запроса на brand с valid_data от водителя (role='d')"""

        valid_data = dict(title='CHANGED TITLE')
        kwargs = {
            'title': brands.first().title
        }
        self._test_update__with_valid_payload_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_data
        )

    def test_update_brand_with_valid_data_by_manager(self, brands, manager):
        """Тест: отправка update-запроса на brand с valid_data от менеджера (role='m')"""

        instance = brands.first()
        kwargs = {'title': instance.title}
        valid_payload = {'title': 'CHANGED TITLE'}

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_payload,
            query_set=brands,
            instance=instance
        )

    # ------------------------ DELETE ------------------------#

    def test_delete_brand_by_anonymous_user(self, brands):
        """Тест: отправка delete-запроса на brand по valid_pk от анонимного пользователя"""

        kwargs = {
            'title': brands.first().title
        }

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, kwargs
        )

    def test_delete_brand_by_UN_privileged_user(self, brands, driver):
        """Тест: отправка delete-запроса на brand по valid_pk от водителя (role='d')"""

        kwargs = {
            'title': brands.first().title
        }
        self._test_delete__with_valid_url_kwargs_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
        )

    def test_delete_brand_with_valid_pk_by_manager(self, brands, manager):
        """Тест: отправка delete-запроса на brand по valid_pk от водителя (role='d')"""

        instance = brands.first()
        kwargs = dict(title=instance.title)
        count = brands.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            instance=instance,
            count=count
        )

##############################
#    TEST's CarAPIViewSet    #
##############################
@pytest.mark.django_db
class TestCarAPIViewSet(BaseTestAPIClass):
    client = APIClient()
    base_path_name = 'car'

    # ------------------------ LIST ------------------------#

    def test_list_cars_by_anonymous_user(self):
        """Тест: отправка list-запроса на cards от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_cars_by_driver(self, driver, manager, brands, cars):
        """Тест: отправка list-запроса на cards от водителя (role='d')"""

        self._test_list__by_UN_privileged_user(driver, self.base_path_name)

    def test_list_cars_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка list-запроса на cards от менеджера (role='m')"""

        self._test_list__by_privileged_user(manager, self.base_path_name, cars)

    # ------------------------ RETRIEVE ------------------------#
    def test_retrieve_car_with_valid_url_kwargs_by_anonymous_user(self, driver, manager, brands, cars):
        """Тест: отправка retrieve-запроса на car с valid_url_kwargs от анонимного пользователя"""

        instance = cars.first()
        kwargs = dict(registration_number=instance.registration_number)
        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, kwargs)

    def test_retrieve_car_with_valid_url_kwargs_by_driver_not_owner(self, driver, manager, brands, cars):
        """Тест: отправка retrieve-запроса на car с valid_url_kwargs от водителя (role='d')"""

        instance = cars.exclude(owner=driver)[0]
        kwargs = dict(registration_number=instance.registration_number)

        self._test_retrieve__with_valid_url_kwarg_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs
        )

    def test_retrieve_car_with_valid_url_kwarg_by_driver_owner(self, driver, manager, brands, cars):
        """Тест: отправка retrieve-запроса на car с valid_url_kwarg от владельца авто"""

        instance = cars.filter(owner=driver)[0]
        kwargs = dict(registration_number=instance.registration_number)

        data = self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs,
            instance=instance,
            fields=['registration_number', 'region_code']
        )
        assert data['brand']['title'] == instance.brand.title
        assert re.search(r"//[^\/]+(.*)", data['owner']).group(1) == reverse('user-detail',
                                                                             kwargs={'email': instance.owner.email})

    def test_retrieve_car_with_valid_url_kwarg_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка retrieve-запроса на car с valid_url_kwarg от менеджера (role='m')"""

        instance = cars.filter(owner=driver)[0]
        kwargs = dict(registration_number=instance.registration_number)

        data = self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs,
            instance=instance,
            fields=['registration_number', 'region_code']
        )

        assert data['brand']['title'] == instance.brand.title
        assert re.search(r"//[^\/]+(.*)", data['owner']).group(1) == reverse('user-detail', kwargs={'email': instance.owner.email})

    def test_retrieve_car_with_IN_valid_pk_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка retrieve-запроса на brand с in_valid_pk от менеджера (role='m')"""

        invalid_kwargs = {'registration_number': 'X000XX'}

        self._test_retrieve__with_IN_invalid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            invalid_url_kwargs=invalid_kwargs
        )

        # ------------------------ CREATE ------------------------#

    def test_create_car_with_valid_data_by_by_anonymous_user(self, driver, manager, brands, cars):
        """Тест: отправка create-запроса на car с valid_data от анонимного пользователя"""

        valid_data = {
            'registration_number': 'X000XX',
            'brand_name': brands.first().title,
            'region_code': 86,
            'last_inspection': '2022-10-12'
        }

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name, valid_data)

    def test_create_car_with_valid_data_by_UN_privileged_user(self, driver, manager, brands, cars):
        """Тест: отправка create-запроса на car с valid_data от водителя (role='d')"""

        valid_data = {
            'registration_number': 'X000XX',
            'brand_name': brands.first().title,
            'region_code': 86,
            'last_inspection': '2022-10-12'
        }

        self._test_create__with_valid_data_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_data=valid_data
        )

    def test_create_car_with_valid_data_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка create-запроса на car с valid_data от менеджера (role='m')"""

        valid_data = {
            'registration_number': 'X000XX',
            'brand_name': brands.get(title='TOYOTA').title,
            'region_code': 86,
            'last_inspection': '2022-10-12'
        }

        data = self._test_create__with_valid_payload_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=cars_models.Car,
            start_count=len(cars)
        )

        assert data['registration_number'] == valid_data['registration_number']
        assert data['region_code'] == valid_data['region_code']
        assert data['brand']['title'] == valid_data['brand_name']
        assert data['owner'] is None
        assert data['last_inspection'] == valid_data['last_inspection']

        instance = cars_models.Car.objects.get(registration_number="X000XX")
        assert valid_data['registration_number'] == instance.registration_number
        assert valid_data['region_code'] == instance.region_code
        assert valid_data['brand_name'] == instance.brand.title
        assert None is instance.owner
        assert valid_data['last_inspection'] == instance.last_inspection.strftime("%Y-%m-%d")


    def test_create_car_with_IN_valid_brand_name_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка create-запроса на car с in_valid_data от менеджера (role='m')"""

        in_valid_data = {
            'registration_number': 'X000XX',
            'brand_name': 'not_brand',
            'region_code': '100',
            'last_inspection': '2021-12-12'
        }
        brand_error = 'brand_not_exist_error'

        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                    base_path_name=self.base_path_name,
                                                                    in_valid_payload=in_valid_data,
                                                                    model=cars_models.CarBrand, start_count=len(brands))

        assert brand_error in data['brand_name'].keys()

    def test_create_car_with_IN_valid_number_and_last_inspection_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка create-запроса на car с in_valid_data от менеджера (role='m')"""

        in_valid_data = {
            'registration_number': 'asdasda',
            'brand_name': 'not_brand',
            'region_code': '100',
            'last_inspection': '2024-12-12'
        }

        registration_number_error_key = 'registration_number_error_key'
        last_inspection_error_key = 'last_inspection_date_error'
        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                           base_path_name=self.base_path_name,
                                                                           in_valid_payload=in_valid_data,
                                                                           model=cars_models.CarBrand,
                                                                           start_count=len(brands))

        assert registration_number_error_key in data['registration_number'].keys()
        assert last_inspection_error_key in data['last_inspection'].keys()

    # ------------------------ UPDATE ------------------------#
    def test_update_car_with_valid_data_by_anonymous_user(self, driver, manager, brands, cars):
        """Тест: отправка update-запроса на car с valid_data от анонимного пользователя"""

        valid_data = {
            'registration_number': 'X000XX',
            'brand_name': brands.get(title='TOYOTA').title,
            'region_code': 86,
            'last_inspection': '2022-10-12'
        }
        kwargs = {
            'registration_number': cars.first().title
        }

        self._test_update__with_valid_payload_by_anonymous_user(
            self.base_path_name, kwargs, valid_data)

    def test_update_car_with_valid_data_by_driver_not_owner(self, driver, manager, brands, cars):
        """Тест: отправка update-запроса на car с valid_data от водителя (role='d')"""

        valid_data = {
            'registration_number': 'X000XX',
            'brand_name': brands.get(title='TOYOTA').title,
            'region_code': 86,
            'last_inspection': '2022-10-12'
        }
        kwargs = {
            'registration_number': cars.exclude(owner=driver)[0]
        }
        self._test_update__with_valid_payload_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_data
        )

    def test_update_card_with_forbidden_fields_by_owner(self, driver, manager, brands, cars):
        """Тест: отправка update-запроса на car с valid_data от водителя (role='d')"""

        instance = cars.filter(owner=driver)[0]

        forbidden_valid_data = {
            'registration_number': 'X000XX',
            'brand_name': brands.get(title='TOYOTA').title,
            'region_code': 86,
        }
        kwargs = {
            'registration_number': instance.registration_number
        }
        updating_error_by_driver = 'update_error'
        data = self._test_update__with_IN_valid_payload_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            in_valid_payload=forbidden_valid_data,
            instance=instance,
            model=type(instance)
        )

        assert updating_error_by_driver in data.keys()

    def test_update_car_with_valid_data_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка update-запроса на brand с valid_data от менеджера (role='m')"""

        instance = cars.filter(owner=driver)[0]

        valid_payload = {
            'registration_number': 'X000XX',
            'brand_name': brands.get(title='TOYOTA').title,
            'region_code': 86,
        }
        kwargs = {
            'registration_number': instance.registration_number
        }

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_payload,
            query_set=cars,
            instance=instance
        )
    # ------------------------ DELETE ------------------------#

    def test_delete_car_by_anonymous_user(self, driver, manager, brands, cars):
        """Тест: отправка delete-запроса на brand по valid_pk от анонимного пользователя"""

        kwargs = {
            'registration_number': cars.first().registration_number
        }

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, kwargs
        )

    def test_delete_car_by_UN_privileged_driver_not_owner(self, driver, manager, brands, cars):
        """Тест: отправка delete-запроса на brand по valid_pk от водителя (role='d')"""

        kwargs = {
            'registration_number': cars.exclude(owner=driver)[0].registration_number
        }
        self._test_delete__with_valid_url_kwargs_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
        )

    def test_delete_car_by_UN_privileged_driver_owner(self, driver, manager, brands, cars):
        """Тест: отправка delete-запроса на brand по valid_pk от водителя (role='d')"""

        kwargs = {
            'registration_number': cars.filter(owner=driver)[0].registration_number
        }
        self._test_delete__with_valid_url_kwargs_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
        )
    def test_delete_car_with_valid_pk_by_manager(self, driver, manager, brands, cars):
        """Тест: отправка delete-запроса на brand по valid_pk от водителя (role='d')"""

        instance = cars.first()
        kwargs = dict(registration_number=instance.registration_number)
        count = cars.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            instance=instance,
            count=count
        )

###############################
#    TEST's UserAPIViewSet    #
###############################

class TestUserAPIViewSet:
    pass


########################################
#    TEST's DocumentTypesAPIViewSet    #
########################################

@pytest.mark.django_db
class TestDocumentTypesAPIViewSet(BaseTestAPIClass):
    client = APIClient()
    base_path_name = 'doc_type'

    # ------------------------ LIST ------------------------#

    def test_list_doc_types_by_anonymous_user(self):
        """Тест: отправка list-запроса на doc_types от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_doc_types_by_driver(self, brands, driver):
        """Тест: отправка list-запроса на doc_types от водителя (role='d')"""

        self._test_list__by_UN_privileged_user(driver, self.base_path_name)

    def test_list_doc_types_by_manager(self, manager, doc_types):
        """Тест: отправка list-запроса на doc_types от менеджера (role='m')"""

        self._test_list__by_privileged_user(manager, self.base_path_name, doc_types)

    # ------------------------ RETRIEVE ------------------------#
    def test_retrieve_doc_types_with_valid_pk_by_anonymous_user(self, manager, doc_types):
        """Тест: отправка retrieve-запроса на doc_types с valid_pk от анонимного пользователя"""

        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, {'pk': 1})

    def test_retrieve_doc_types_with_valid_pk_by_driver(self, driver, doc_types):
        """Тест: отправка retrieve-запроса на doc_types с valid_pk от водителя (role='d')"""

        self._test_retrieve__with_valid_url_kwarg_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwarg={'pk': 1}
        )

    def test_retrieve_doc_types_with_valid_pk_by_manager(self, manager, doc_types):
        """Тест: отправка retrieve-запроса на doc_types с valid_pk от менеджера (role='m')"""

        kwargs = {'pk': doc_types.first().pk}
        instance = doc_types.get(pk=kwargs['pk'])

        self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs,
            instance=instance,
            fields=['title', 'car_or_user']
        )

    def test_retrieve_doc_types_with_IN_valid_pk_by_manager(self, manager, doc_types):
        """Тест: отправка retrieve-запроса на doc_types с in_valid_pk от менеджера (role='m')"""

        invalid_kwargs = {'pk': 1000}

        self._test_retrieve__with_IN_invalid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            invalid_url_kwargs=invalid_kwargs
        )

    # ------------------------ CREATE ------------------------#

    def test_create_doc_type_with_valid_data_by_by_anonymous_user(self, doc_types):
        """Тест: отправка create-запроса на doc_type с valid_data от анонимного пользователя"""

        valid_data = dict(title='NEW DOC TYPE', car_or_user='c')

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name, valid_data)

    def test_create_doc_type_with_valid_data_by_by_UN_privileged_user(self, doc_types, driver):
        """Тест: отправка create-запроса на doc_type с valid_data от водителя (role='d')"""

        valid_data = dict(title='NEW DOC TYPE', car_or_user='c')

        self._test_create__with_valid_data_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_data=valid_data
        )

    def test_create_user_doc_type_with_valid_data_by_manager(self, manager, doc_types):
        """Тест: отправка create-запроса на doc_type с valid_data (user) от менеджера (role='m')"""

        valid_data = dict(title='NEW DOC TYPE', car_or_user='m')

        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=base_models.DocType,
            start_count=doc_types.count()
        )

    def test_create_car_doc_type_with_valid_data_by_manager(self, manager, doc_types):
        """Тест: отправка create-запроса на doc_type с valid_data (car) от менеджера (role='m')"""

        valid_data = dict(title='NEW DOC TYPE', car_or_user='c')

        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=base_models.DocType,
            start_count=len(doc_types)
        )


    def test_create_doc_type_with_IN_valid_data_by_manager(self, manager, doc_types):
        """Тест: отправка create-запроса на doc_type с valid_data от менеджера (role='m')"""

        in_valid_data = dict(title='NEW DOC TYPE with incorrect type', car_or_user='t')

        self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                    base_path_name=self.base_path_name,
                                                                    in_valid_payload=in_valid_data,
                                                                    model=base_models.DocType,
                                                                    start_count=len(doc_types))


    # ------------------------ UPDATE ------------------------#

    def test_update_doc_type_with_valid_data_by_by_anonymous_user(self, doc_types):
        """Тест: отправка update-запроса на doc_type с valid_data от анонимного пользователя"""

        valid_data = dict(title='NEW DOC TYPE')
        kwargs = {
            'pk': doc_types.first().pk
        }

        self._test_update__with_valid_payload_by_anonymous_user(
            self.base_path_name, kwargs, valid_data)

    def test_update_doc_type_with_valid_data_by_by_UN_privileged_user(self, doc_types, driver):
        """Тест: отправка update-запроса на doc_type с valid_data от водителя (role='d')"""

        valid_data = dict(title='NEW DOC TYPE')
        kwargs = {
            'pk': doc_types.first().pk
        }
        self._test_update__with_valid_payload_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_data
        )

    def test_update_doc_type_with_valid_data_by_by_manager(self, doc_types, manager):
        """Тест: отправка update-запроса на doc_type с valid_data от менеджера (role='m')"""

        instance = doc_types.first()
        kwargs = {'pk': instance.pk}
        valid_data = dict(title='NEW DOC TYPE', car_or_user='c')

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_data,
            query_set=doc_types,
            instance=instance
        )

    def test_update_doc_type_with_IN_valid_car_or_user_by_by_manager(self, doc_types, manager):
        """Тест: отправка update-запроса на doc_type с in_valid_data от менеджера (role='m')"""

        instance = doc_types.first()

        kwargs = {'pk': instance.pk}
        in_valid_payload = {'title': 'NEW DOC TITLE', 'car_or_user': 'd'}

        self._test_update__with_IN_valid_payload_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            in_valid_payload=in_valid_payload,
            instance=instance,
            model=base_models.DocType
        )

    # ------------------------ DELETE ------------------------#

    def test_delete_doc_type_by_anonymous_user(self, doc_types):
        """Тест: отправка delete-запроса на doc_types по valid_pk от анонимного пользователя"""

        instance = doc_types.first()
        kwargs = dict(pk=instance.pk)

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, kwargs
        )

    def test_delete_doc_type_by_UN_privileged_user(self, doc_types, driver):
        """Тест: отправка delete-запроса на doc_types по valid_pk от водителя (role='d')"""

        instance = doc_types.first()
        kwargs = dict(pk=instance.pk)

        self._test_delete__with_valid_url_kwargs_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
        )

    def test_delete_doc_type_with_valid_pk_by_manager(self, doc_types, manager):
        """Тест: отправка delete-запроса на doc_types по valid_pk от водителя (role='d')"""

        instance = doc_types.first()
        kwargs = dict(pk=instance.pk)
        count = doc_types.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            instance=instance,
            count=count
        )

######################################
#    TEST's CarDocumentAPIViewSet    #
######################################

class TestCarDocumentAPIViewSet:
    pass


#######################################
#    TEST's UserDocumentAPIViewSet    #
#######################################

class TestUserDocumentAPIViewSet:
    pass


########################################
#    TEST's RepairRequestAPIViewSet    #
########################################

class TestRepairRequestAPIViewSet:
    pass


################################
#    TEST's CardsAPIViewSet    #
################################

@pytest.mark.django_db
class TestCardsAPIViewSet(BaseTestAPIClass):
    client = APIClient()
    base_path_name = 'card'

    # ------------------------ LIST ------------------------#

    def test_list_cards_by_anonymous_user(self):
        """Тест: отправка list-запроса на cards от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_cards_by_driver(self, driver, manager, cards):
        """Тест: отправка list-запроса на cards от водителя (role='d')"""

        self._test_list__by_UN_privileged_user(driver, self.base_path_name)

    def test_list_cards_by_manager(self, driver, manager, cards):
        """Тест: отправка list-запроса на cards от менеджера (role='m')"""

        self._test_list__by_privileged_user(manager, self.base_path_name, cards)

    # ------------------------ RETRIEVE ------------------------#
    def test_retrieve_card_with_valid_pk_by_anonymous_user(self, driver, manager, cards):
        """Тест: отправка retrieve-запроса на card с valid_pk от анонимного пользователя"""

        instance = cards.filter(owner=driver)[0]
        kwargs = dict(number=instance.number)

        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, kwargs)

    def test_retrieve_card_with_valid_pk_by_driver_NOT_owner(self, driver, manager, cards):
        """Тест: отправка retrieve-запроса на card с valid_pk от водителя (role='d')"""

        instance = cards.exclude(owner=driver)[0]
        kwargs = dict(number=instance.number)

        self._test_retrieve__with_valid_url_kwarg_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs
        )

    def test_retrieve_card_with_valid_pk_by_driver_owner(self, driver, manager, cards):
        """Тест: отправка retrieve-запроса на card с valid_pk от менеджера (role='m')"""

        instance = cards.filter(owner=driver)[0]
        kwargs = dict(number=instance.number)

        self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs,
            instance=instance,
            fields=['number', 'limit', 'balance', 'owner']
        )

    def test_retrieve_card_with_valid_pk_by_manager(self, driver, manager, cards):
        """Тест: отправка retrieve-запроса на card с valid_pk от менеджера (role='m')"""

        instance = cards.filter(owner=driver)[0]
        kwargs = dict(number=instance.number)

        self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwarg=kwargs,
            instance=instance,
            fields=['number', 'limit', 'balance', 'owner']
        )

    def test_retrieve_card_with_IN_valid_pk_by_manager(self, driver, manager, cards):
        """Тест: отправка retrieve-запроса на card с in_valid_pk от менеджера (role='m')"""

        invalid_kwargs = dict(number='0000000000000000')

        self._test_retrieve__with_IN_invalid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            invalid_url_kwargs=invalid_kwargs
        )


    # # ---------------------- FILTATRION ----------------------#
    #
    # def test_filter_cards_by_manager(self, driver, manager, cards):
    #     """Тест: отправка list-запроса на cards от менеджера (role='m')"""
    #
    #     self.client.force_login(manager)
    #     url = reverse(f'{self.base_path_name}-list')
    #
    #     response = self.client.get(url, {'number': '1234'})
    #     data = response.data
    #
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(data) == len(account_models.FuelCard.objects.count())



    # ------------------------ CREATE ------------------------#

    def test_create_card_with_valid_data_by_by_anonymous_user(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с valid_data от анонимного пользователя"""

        valid_data = dict(
            limit=1000,
            number='0000000000000000',
        )

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name, valid_data)

    def test_create_card_with_valid_data_by_by_UN_privileged_user(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с valid_data от водителя (role='d')"""

        valid_data = dict(
            limit=1000,
            number='0000000000000000',
        )

        self._test_create__with_valid_data_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_data=valid_data
        )

    def test_create_card_with_valid_data_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с valid_data от менеджера (role='m')"""

        valid_data = dict(
            limit=1000,
            number='0000000000000000',
        )

        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=account_models.FuelCard,
            start_count=cards.count()
        )

    def test_create_card_with_IN_valid_data_used_owner_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с in_valid_data (used driver) от менеджера (role='m')"""

        in_valid_data = dict(
            limit=1000,
            number='0000000000000000',
            owner=driver.pk,
        )
        owner_error_code = 'unique'
        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                    base_path_name=self.base_path_name,
                                                                    in_valid_payload=in_valid_data,
                                                                    model=account_models.FuelCard,
                                                                    start_count=len(cards),
                                                                    )

        assert owner_error_code == data['owner'][0].code
    def test_create_card_with_IN_valid_data_incorrect_number_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с in_valid_data (неккоректного номера) от менеджера (role='m')"""

        in_valid_data = dict(
            limit=1000,
            number='asdsadasasdas',
        )
        number_error_key = 'invalid_number_error'
        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                    base_path_name=self.base_path_name,
                                                                    in_valid_payload=in_valid_data,
                                                                    model=account_models.FuelCard,
                                                                    start_count=len(cards),
                                                                    )
        assert number_error_key in data['number'].keys()
    def test_create_card_with_IN_valid_data_limit_less_balance_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с in_valid_data (Лимит меньше баланса) от менеджера (role='m')"""


        in_valid_data = dict(
            limit=1000,
            balance=2000,
            number='0000000000000000',
        )
        balance_and_limit_error_key = 'balance_and_limit_error'

        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                           base_path_name=self.base_path_name,
                                                                           in_valid_payload=in_valid_data,
                                                                           model=account_models.FuelCard,
                                                                           start_count=len(cards)
                                                                          )
        assert balance_and_limit_error_key in data.keys()

    # ------------------------ UPDATE ------------------------#

    def test_update_card_with_valid_data_by_anonymous_user(self, driver, manager, cards):
        """Тест: отправка update-запроса на card с valid_data от анонимного пользователя"""

        valid_data = dict(
            limit=1000,
            number='0000000000000000',
        )
        kwargs = {
            'number': cards.first().number
        }

        self._test_update__with_valid_payload_by_anonymous_user(
            self.base_path_name, kwargs, valid_data)

    def test_update_card_with_forbidden_field_number_by_owner(self, driver, manager, cards):
        """Тест: отправка update-запроса на card запрещенным полем number от owner (role='d')"""

        instance = cards.filter(owner=driver)[0]
        in_valid_payload = dict(
            number='0000000000000000',
        )
        kwargs = {
            'number': instance.number
        }
        updating_error_by_driver = 'update_error'

        data = self._test_update__with_IN_valid_payload_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            in_valid_payload=in_valid_payload,
            instance=instance,
            model=account_models.FuelCard
        )
        assert updating_error_by_driver in data.keys()


    def test_update_card_with_forbidden_field_limit_by_owner(self, driver, manager, cards):
        """Тест: отправка update-запроса на card запрещенным полем limit от owner (role='d')"""

        instance = cards.filter(owner=driver)[0]
        in_valid_payload = dict(
            limit=9999,
        )
        kwargs = {
            'number': instance.number
        }
        updating_error_by_driver = 'update_error'

        data = self._test_update__with_IN_valid_payload_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            in_valid_payload=in_valid_payload,
            instance=instance,
            model=account_models.FuelCard
        )
        assert updating_error_by_driver in data.keys()

    def test_update_card_with_with_forbidden_field_owner_limit_by_owner(self, driver, manager, cards):
        """Тест: отправка update-запроса на card запрещенным полем limit от owner (role='d')"""

        instance = cards.filter(owner=driver)[0]
        in_valid_payload = dict(
            owner=None,
        )
        kwargs = {
            'number': instance.number
        }
        updating_error_by_driver = 'update_error'

        data = self._test_update__with_IN_valid_payload_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            in_valid_payload=in_valid_payload,
            instance=instance,
            model=account_models.FuelCard
        )
        assert updating_error_by_driver in data.keys()

    def test_update_card_with_with_invalid_balance_by_owner(self, driver, manager, cards):
        """Тест: отправка update-запроса на card invalid_balance от owner (role='d')"""

        instance = cards.filter(owner=driver)[0]
        in_valid_payload = {
            'balance': instance.limit + 1000000,
        }
        kwargs = {
            'number': instance.number
        }
        updating_error_by_driver = 'balance_and_limit_error'

        data = self._test_update__with_IN_valid_payload_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            in_valid_payload=in_valid_payload,
            instance=instance,
            model=account_models.FuelCard
        )
        assert updating_error_by_driver in data.keys()

    def test_update_card_with_valid_balance_by_owner(self, driver, manager, cards):
        """Тест: отправка update-запроса на card с valid_balance от owner"""

        instance = cards.filter(owner=driver)[0]
        valid_data = {
            'balance': instance.limit - 100
        }
        kwargs = {
            'number': instance.number
        }

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_data,
            instance=instance,
            query_set=cards
        )

    def test_update_card_with_valid_data_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с valid_data от менеджера (role='m')"""

        instance = cards.filter(owner=driver)[0]

        valid_data = dict(
            limit=999,
            number='0000000000000000',
            owner=None,
        )
        kwargs = {
            'number': instance.number
        }

        data = self._test_update__with_valid_data_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            valid_payload=valid_data,
            instance=instance,
            query_set=cards
        )

    def test_update_card_with_IN_valid_data_used_owner_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с in_valid_data (used driver) от менеджера (role='m')"""

        instance = cards.filter(owner=driver)[0]
        kwargs = {
            'number': instance.number
        }
        in_valid_data = dict(
            limit=1000,
            number='0000000000000000',
            owner=manager.pk,
        )
        owner_error_code = 'unique'
        data = self._test_update__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                           base_path_name=self.base_path_name,
                                                                           valid_url_kwargs=kwargs,
                                                                           in_valid_payload=in_valid_data,
                                                                           instance=instance,
                                                                           model=account_models.FuelCard
                                                                           )

        assert owner_error_code == data['owner'][0].code

    def test_update_card_with_IN_valid_data_incorrect_number_by_manager(self, driver, manager, cards):
        """Тест: отправка update-запроса на card с in_valid_data (неккоректного номера) от менеджера (role='m')"""

        instance = cards.first()
        kwargs = {
            'number': instance.number
        }
        in_valid_data = dict(
            limit=1000,
            number='asdsadasasdas',
        )
        number_error_key = 'invalid_number_error'
        data = self._test_update__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                           base_path_name=self.base_path_name,
                                                                           valid_url_kwargs=kwargs,
                                                                           in_valid_payload=in_valid_data,
                                                                           instance=instance,
                                                                           model=account_models.FuelCard
                                                                           )

        assert number_error_key in data['number'].keys()



    def test_update_card_with_IN_valid_data_limit_less_balance_by_manager(self, driver, manager, cards):
        """Тест: отправка create-запроса на card с in_valid_data (Лимит меньше баланса) от менеджера (role='m')"""

        instance = cards.first()
        kwargs = {
            'number': instance.number
        }
        in_valid_data = dict(
            limit=1000,
            balance=2000,
            number='0000000000000000',
        )
        balance_and_limit_error_key = 'balance_and_limit_error'
        data = self._test_update__with_IN_valid_payload_by_privileged_user(prv_user=manager,
                                                                           base_path_name=self.base_path_name,
                                                                           valid_url_kwargs=kwargs,
                                                                           in_valid_payload=in_valid_data,
                                                                           instance=instance,
                                                                           model=account_models.FuelCard
                                                                           )

        assert balance_and_limit_error_key in data.keys()

    # ------------------------ DELETE ------------------------#

    def test_delete_card_by_anonymous_user(self,  driver, manager, cards):
        """Тест: отправка delete-запроса на card по valid_pk от анонимного пользователя"""

        instance = cards.first()
        kwargs = dict(number=instance.number)

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, kwargs
        )

    def test_delete_card_by_UN_privileged_driver_NOT_owner(self, driver, manager, cards):
        """Тест: отправка delete-запроса на card по cards от НЕ_владельца водителя (role='d')"""

        instance = cards.exclude(owner=driver)[0]
        kwargs = dict(number=instance.number)

        self._test_delete__with_valid_url_kwargs_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
        )

    def test_delete_card_by_UN_privileged_driver_owner(self, driver, manager, cards):
        """Тест: отправка delete-запроса на card по cards от НЕ_владельца водителя (role='d')"""

        instance = cards.filter(owner=driver)[0]
        kwargs = dict(number=instance.number)

        self._test_delete__with_valid_url_kwargs_by_UN_privileged_user(
            un_prv_user=driver,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
        )

    def test_delete_card_with_valid_pk_by_manager(self, driver, manager, cards):
        """Тест: отправка delete-запроса на card по valid_pk от водителя (role='d')"""

        instance = cards.first()
        kwargs = dict(number=instance.number)
        count = cards.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=manager,
            base_path_name=self.base_path_name,
            valid_url_kwargs=kwargs,
            instance=instance,
            count=count
        )




#######################################
#    TEST's NotificationAPIViewSet    #
#######################################

class TestNotificationAPIViewSet:
    pass
