from app.main.service.sensor_type_service import SensorTypeService


def test_get_sensor_type_info_should_return_sensor_info_when_valid_request(
        get_sensor_type_default_values,
        create_sensor_type,
        create_device_group,
        create_user_group):
    sensor_type_service_instance = SensorTypeService.get_instance()

    device_group = create_device_group()

    sensor_type = create_sensor_type()


    user_group = create_user_group()

