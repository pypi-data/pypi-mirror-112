
#pragma once

#include <string>
#include <vector>

#include "Entity.h"
#include "EntityTenantMixin.h"
#include "EntityDateMixin.h"
#include "Paging.h"
#include "EntityCollection.h"



namespace BAScloud {

class Device;

/** 
 * A SetPoint entity represents a future set point for a sensor or actor (Device) in a building (Property).
 * 
 * Each SetPoint has an associated Device, a value, and a timestamp.
 * 
 */
class SetPoint : public Entity, public EntityTenantMixin, public EntityDateMixin {

 private:
 
  /**
   * Time of the entity value for the SetPoint.
   */
   std::time_t timestamp;

  /**
   * Value of the sensor or actor (Device) at a given timestamp.
   */
   double value;

 public:

   /**
    * SetPoint constructor
    *
    * Creates a SetPoint object representing a BAScloud API entity.
    *
    * Note: Creating an entity object over its constructor does not automatically create the entity in the BAScloud. 
    * For creation of a BAScloud entity use the static method of the corresponding object class SetPoint::createSetPoint().
    *
    * @param API_UUID Universally unique identifier of the represented BAScloud SetPoint.
    * @param API_tenant_UUID Universally unique identifier of the represented BAScloud SetPoint.
    * @param value Value of the SetPoint.
    * @param timestamp Timestamp of the SetPoint.
    * @param createdAt Datetime describing the creation of the SetPoint entity in the BAScloud.
    * @param updatedAt Datetime describing the last update of the SetPoint information in the BAScloud.
    * @param context EntityContext proving an abstracted context for accessing the API functions.
    */
   SetPoint(std::string API_UUID, std::string API_tenant_UUID, double value, std::time_t timestamp, std::time_t createdAt, std::time_t updatedAt, EntityContext* context);

  /**
   * Get the SetPoint value.
   * 
   * @return Double precision floating point value of the SetPoint.
   */
   double getValue();

  /**
   * Get the time of the SetPoint of the entity value.
   * 
   * @return UNIX timestamp value.
   */
   std::time_t getTimestamp();

   /**
    * Get the associated Device entity of the SetPoint.
    * 
    * @throws ServerError
    * @throws ConnectionError
    * @throws BadRequest
    * @throws UnauthorizedRequest
    * @throws NotFoundRequest
    * @throws ConflictRequest
    * @throws InvalidResponse
    * 
    * @return Device entity object of the associated BAScloud Device.
    */
	 Device getAssociatedDevice();

   /**
    * Request a single SetPoint entity.
    * 
    * A SetPoint is uniquely identified by the associated Tenant and SetPoint UUID.
    * 
    * @throws ServerError
    * @throws ConnectionError
    * @throws BadRequest
    * @throws UnauthorizedRequest
    * @throws NotFoundRequest
    * @throws ConflictRequest
    * @throws InvalidResponse
    * 
    * @param API_tenant_UUID UUID of the associated BAScloud Tenant of the SetPoint.
    * @param API_setpoint_UUID UUID of the represented BAScloud SetPoint.
    * @param context EntityContext proving an abstracted context for accessing the API functions.
    * 
    * @return A SetPoint object representing the BAScloud SetPoint with the specified UUID.
    */
   static SetPoint getSetPoint(std::string API_tenant_UUID, std::string API_setpoint_UUID, EntityContext* context);

  /**
    * Request a collection of SetPoint entities grouped under the given Tenant.
    * 
    * The request filters the BAScloud SetPoint based on the given parameters and returns a collection 
    * of SetPoint matching these values.
    * 
    * @throws ServerError
    * @throws ConnectionError
    * @throws BadRequest
    * @throws UnauthorizedRequest
    * @throws NotFoundRequest
    * @throws ConflictRequest
    * @throws InvalidResponse
    * 
    * @param API_tenant_UUID UUID of the associated BAScloud Tenant.
    * @param context EntityContext proving an abstracted context for accessing the API functions.
    * @param paging Optional PagingOption that is used for requesting paged API results.
    * @param from Optional filter defining the start time of a time-range the requested SetPoint should lie in.
    * @param until Optional filter defining the end time of a time-range the requested SetPoint should lie in.
    * @param timestamp Optional filter for the timestamp of the SetPoint.
    * @param currentTime Optional filter for the current time.
    * @param API_device_UUID Optional filter for the associated Device UUID of the SetPoint.
    * @param createdFrom Optional filter for the creation date of the SetPoint. All points from this timestamp.
    * @param createdUntil Optional filter for the creation date of the SetPoint. All points until this timestamp.
    * 
    * @return EntityCollection containing list of SetPoint entities matching the provided filters and paging information.
    */
   static EntityCollection<SetPoint> getSetPoints(std::string API_tenant_UUID, EntityContext* context, PagingOption paging={}, std::time_t from=-1, std::time_t until=-1, std::time_t timestamp=-1, std::time_t currentTime=-1, std::string API_device_UUID={}, std::time_t createdFrom=-1, std::time_t createdUntil=-1);

   /**
    * Create a new SetPoint entity in the BAScloud.
    * 
    * Given the associated Tenant and Device entity, a new SetPoint is created using the given SetPoint parameter.
    * 
    * @throws ServerError
    * @throws ConnectionError
    * @throws BadRequest
    * @throws UnauthorizedRequest
    * @throws NotFoundRequest
    * @throws ConflictRequest
    * @throws InvalidResponse
    * 
    * @param API_tenant_UUID UUID of the associated BAScloud Tenant of the SetPoint.
    * @param API_device_UUID UUID of the associated BAScloud Device of the SetPoint.
    * @param value Value of the SetPoint
    * @param timestamp The time of the SetPoint value.
    * @param context EntityContext proving an abstracted context for accessing the API functions.
    * 
    * @return SetPoint entity object representing the newly created BAScloud SetPoint.
    */
   static SetPoint createSetPoint(std::string API_tenant_UUID, std::string API_device_UUID, double value, std::time_t timestamp, EntityContext* context);

   /**
    * Updates an existing SetPoint entity in the BAScloud. [Admin]
    * 
    * Can update the SetPoint's value, timestamp or device relationship
    * 
    * @throws ServerError
    * @throws ConnectionError
    * @throws BadRequest
    * @throws UnauthorizedRequest
    * @throws NotFoundRequest
    * @throws ConflictRequest
    * @throws InvalidResponse
    * 
    * @param API_tenant_UUID UUID of the associated BAScloud Tenant of the SetPoint.
    * @param API_setpoint_UUID UUID of the existing BAScloud SetPoint that is supposed to be updated.
    * @param context EntityContext proving an abstracted context for accessing the API functions.
    * @param value Optional update of the SetPoints value.
    * @param timestamp Optional update for the timestamp of the SetPoint.
    * @param API_device_UUID Optional relationship update for the associated device of the SetPoint.
    * @return List of SetPoint entities representing the newly created BAScloud SetPoint. Unsuccessfull creations will be null.
    */
    void updateSetpoint(std::string API_tenant_UUID, std::string API_setpoint_UUID, EntityContext* context, double value=std::numeric_limits<double>::quiet_NaN(), std::time_t timestamp=-1, std::string API_device_UUID={});

   /**
    * Deletes an existing SetPoint in the BAScloud. [Admin] 
    * 
    * The request deletes a SetPoint entity in the BAScloud based on the given SetPoint UUID.
    * This operation needs administration authority. 
    * 
    * @throws ServerError
    * @throws ConnectionError
    * @throws BadRequest
    * @throws UnauthorizedRequest
    * @throws NotFoundRequest
    * @throws ConflictRequest
    * @throws InvalidResponse
    * 
    * @param API_tenant_UUID UUID of the associated BAScloud Tenant of the SetPoint.
    * @param API_reading_UUID UUID of the existing BAScloud SetPoint that is supposed to be deleted.
    * @param context EntityContext proving an abstracted context for accessing the API functions.
    */
	 static void deleteSetpoint(std::string API_tenant_UUID, std::string API_setpoint_UUID, EntityContext* context);


};

}