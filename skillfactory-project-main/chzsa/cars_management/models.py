from django.db import models


class ServiceCompany(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Technics(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'technics'


class EngineModels(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'engine_models'


class TransmissionModels(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'transmission_models'


class SteeringAxleType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'front_axle_models'


class DriveAxleType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'rear_axle_models'


class MaintenanceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'maintenance_types'


class ComplaintType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'complaint_types'


class RestorationMethods(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'restoration_methods'


class Car(models.Model):
    factory_number = models.CharField(unique=True, max_length=255)
    model = models.ForeignKey(Technics, on_delete=models.CASCADE)
    engine_type = models.ForeignKey(EngineModels, on_delete=models.CASCADE)
    engine_id = models.CharField(max_length=255)
    transmission_type = models.ForeignKey(TransmissionModels, on_delete=models.CASCADE)
    transmission_id = models.CharField(max_length=255)
    drive_axle_type = models.ForeignKey(DriveAxleType, on_delete=models.CASCADE)
    drive_axle_id = models.CharField(max_length=255)
    steering_axle_type = models.ForeignKey(SteeringAxleType, on_delete=models.CASCADE)
    steering_axle_id = models.CharField(max_length=255)
    supply_contract_data = models.CharField(max_length=255)
    shipment_date = models.DateField()
    consignee = models.CharField(max_length=255)
    consignee_address = models.CharField(max_length=255)
    car_config = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE)

    class Meta:
        ordering = ['shipment_date']


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    operating_hours = models.DecimalField(max_digits=10, decimal_places=2)
    work_order_number = models.CharField(max_length=255)
    work_order_date = models.DateField()
    service_organization = models.CharField(max_length=255)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE)

    class Meta:
        ordering = ['maintenance_date']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Reclamation(models.Model):
    date_of_failure = models.DateField()
    operating_hours = models.DecimalField(max_digits=10, decimal_places=2)
    failure_node = models.ForeignKey(ComplaintType, on_delete=models.CASCADE)
    failure_description = models.TextField()
    restoration_method = models.ForeignKey(RestorationMethods, on_delete=models.CASCADE)
    used_spare_parts = models.TextField()
    restoration_date = models.DateField()
    downtime_hours = models.DecimalField(max_digits=10, decimal_places=2)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_of_failure']

    def save(self, *args, **kwargs):
        self.downtime_hours = (self.restoration_date - self.date_of_failure).total_seconds() / 3600
        super().save(*args, **kwargs)