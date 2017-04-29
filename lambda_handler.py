def lambda_handler(event, context):
    #access_token = event['payload']['accessToken']
    namespace    = event['header']['namespace']

    dispatch = handleDiscovery if namespace == 'Alexa.ConnectedHome.Discovery' else handleControl
    return dispatch(context, event)


def handleDiscovery(context, event):
    payload = ''
    header = {
        "namespace": "Alexa.ConnectedHome.Discovery",
        "name": "DiscoverAppliancesResponse",
        "payloadVersion": "2"
    }

    if event['header']['name'] == 'DiscoverAppliancesRequest':
        payload = {
            "discoveredAppliances": [
                {
                    "applianceId":                "device001",
                    "manufacturerName":           "yourManufacturerName",
                    "modelName":                  "model 01",
                    "version":                    "your software version number here.",
                    "friendlyName":               "Smart Home Virtual Device",
                    "friendlyDescription":        "Virtual Device for the Sample Hello World Skill",
                    "isReachable":                True,
                    "actions":                    [
                        "turnOn",
                        "turnOff",
                    ],
                    "additionalApplianceDetails": {
                        "extraDetail1": "optionalDetailForSkillAdapterToReferenceThisDevice",
                        "extraDetail2": "There can be multiple entries",
                        "extraDetail3": "but they should only be used for reference purposes.",
                        "extraDetail4": "This is not a suitable place to maintain current device state"
                    },
                }
            ]
        }
    return { 'header': header, 'payload': payload }
    
    
    
def handleControl(context, event):
    device_id    = event['payload']['appliance']['applianceId']
    event_header = event['header']
    message_id   = event_header['messageId']
    payload      = {} if event_header['name'] == 'TurnOnRequest' else ''
    header       = {
        "namespace":      "Alexa.ConnectedHome.Control",
        "name":           "TurnOnConfirmation",
        "payloadVersion": "2",
        "messageId":      message_id
    }

    return { 'header': header, 'payload': payload }
