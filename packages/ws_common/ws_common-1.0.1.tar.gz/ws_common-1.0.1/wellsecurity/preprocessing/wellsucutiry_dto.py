class WSTypeQualificationException(Exception):
    pass


class ObjectType:
    rectangle = "rectangle"
    polygon = "polygon"


class Point:
    def __init__(self, x: str = None, y: str = None, z: str = None, additional_data: str = None):
        self.x = x
        self.y = y
        self.z = z
        self.additional_data = additional_data


class PointList(list):
    def append(self, temp_object):
        if type(temp_object) is not Point:
            raise WSTypeQualificationException("The type must be Point.")
        super().append(temp_object)


class InferenceResult:
    def __init__(self, id: str, name: str, point_list: PointList, confidence: str, object_type: ObjectType):
        self.id = id
        self.name = name
        self.point_list = point_list
        self.confidence = confidence
        self.object_type = object_type


class InferenceResultList(list):
    def append(self, temp_object):
        if type(temp_object) is not InferenceResult:
            raise WSTypeQualificationException("The type must be InferenceResult.")
        super().append(temp_object)


class PictureAddressList(list):
    def append(self, temp_object):
        if type(temp_object) is not str:
            raise WSTypeQualificationException("The type must be str.")
        super().append(temp_object)


class MessageData:
    def __init__(self, stream_address: str, video_address: str, picture_address_list: PictureAddressList,
                 inference_result_list: InferenceResultList):
        self.stream_address = stream_address
        self.video_address = video_address
        self.picture_address_list = picture_address_list
        self.inference_result_list = inference_result_list


class MessageType:
    wellsucurity = "wellsucurity"
    unknown = "unknown"
    testing = "testing"


class MessageProducerState:
    def __init__(self, start=True, intermediate=False, end=False, id: str = None, signature: str = None):
        self.start = start
        self.intermediate = intermediate
        self.end = end
        self.id = id
        self.signature = signature


class MessageConsumerState:
    def __init__(self, start=True, intermediate=False, end=False, id: str = None, signature: str = None):
        self.start = start
        self.intermediate = intermediate
        self.end = end
        self.id = id
        self.signature = signature


class MessageConsumerStateList(list):
    def append(self, temp_object):
        if type(temp_object) is not MessageConsumerState:
            raise WSTypeQualificationException("The type must be MessageConsumerState.")
        super().append(temp_object)


class Message:
    def __init__(self, message_id: str = None, start_timestamp: str = None, end_timestamp: str = None,
                 message_producer_state: MessageProducerState = None,
                 message_consumer_state_list: MessageConsumerStateList = None,
                 message_type: str = None,
                 message_data: MessageData = None, additional_data: dict = None):
        self.message_id = message_id
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.message_producer_state = message_producer_state
        self.message_consumer_state_list = message_consumer_state_list
        self.message_type = message_type
        self.message_data = message_data
        self.additional_data = additional_data

    # def __repr__(self):
    #     return repr((self.message_id, self.start_timestamp, self.end_timestamp))


class WSJsonUtils():
    def __init__(self):
        self.jresult = ""

    def loopKV(self, x):
        if hasattr(x, "__dict__"):
            for temp in x.__dict__:
                k1 = x.__getattribute__(temp)
                if isinstance(k1, int) or isinstance(k1, float) or isinstance(k1, str) or isinstance(k1, bool) or k1 is None:
                    #print(str(temp) + "______" + str(k1) + "______" + str(type(k1)))
                    self.jresult += '"' + str(temp) + '"' + ":" + '"' + str(k1) + '"' + ","
                    pass
                elif isinstance(k1, list):
                    self.jresult += '"' + str(temp) + '"' + ":" + '['
                    for k2 in k1:
                        self.jresult += '{'
                        self.loopKV(k2)
                        self.jresult += '}' + ","
                    self.jresult += ']' + ","
                elif isinstance(k1, set):
                    #print(k1)
                    pass
                elif isinstance(k1, dict):
                    #print(k1)
                    pass
                else:
                    self.jresult += '"' + str(temp) + '"' + ":" + '{'
                    self.loopKV(k1)
                    self.jresult += '}' + ","
        else:
            # print(x)
            pass

    def transfer2json(self, content):
        self.loopKV(content)
        result = "{" + self.jresult + "}"
        import re
        result = re.compile(",}").sub("}", result)
        result = re.compile(",]").sub("]", result)
        return result


if __name__ == '__main__':
    pointList = PointList(list())
    pointList.append(Point(100, 111))
    pointList.append(Point(200, 211))

    inferenceResult1 = InferenceResult(id="1000001", name="no_vest", point_list=pointList, confidence="0.99",
                                       object_type=ObjectType.rectangle)
    inferenceResult2 = InferenceResult(id="1000002", name="no_helmet", point_list=pointList, confidence="0.61",
                                       object_type=ObjectType.rectangle)
    inferenceResult3 = InferenceResult(id="1000003", name="pedestrian", point_list=pointList, confidence="0.47",
                                       object_type=ObjectType.rectangle)

    inferenceResultList = InferenceResultList(list())
    inferenceResultList.append(inferenceResult1)
    inferenceResultList.append(inferenceResult2)
    inferenceResultList.append(inferenceResult3)

    pictureAddressList = PictureAddressList(list())
    pictureAddressList.append("http://a.com/wellsecurity/yantian/static/2021/06/28/07/33/camera1001/aaa1.jpg")
    pictureAddressList.append("http://a.com/wellsecurity/yantian/static/2021/06/28/07/33/camera1001/aaa2.jpg")
    pictureAddressList.append("http://a.com/wellsecurity/yantian/static/2021/06/28/07/33/camera1001/aaa3.jpg")

    messageData = MessageData(stream_address="rtsp://192.168.110.66", video_address="http://10.66.8.24/vvvv.mp4",
                              picture_address_list=pictureAddressList, inference_result_list=inferenceResultList)

    messageProducerState = MessageProducerState(start=True, intermediate=True, end=False, id="1001",
                                                signature="wwwwww")

    messageConsumerState1 = MessageConsumerState(start=True, intermediate=True, end=False, id="2001",
                                                 signature="dfsdfdsf")
    messageConsumerState2 = MessageConsumerState(start=True, intermediate=True, end=False, id="2002",
                                                 signature="mmmmmmmk")
    messageConsumerState3 = MessageConsumerState(start=True, intermediate=True, end=False, id="2003",
                                                 signature="vvvvvvvv")
    messageConsumerStateList = MessageConsumerStateList()
    messageConsumerStateList.append(messageConsumerState1)
    messageConsumerStateList.append(messageConsumerState2)
    messageConsumerStateList.append(messageConsumerState3)

    message = Message(message_id="9854215645555", start_timestamp="123504578", end_timestamp=None,
                      message_producer_state=messageProducerState, message_consumer_state_list=messageConsumerStateList,
                      message_type=MessageType.testing, message_data=messageData,
                      additional_data={"via": "yie", "fly": "fly"})

    wSJsonUtils = WSJsonUtils()
    temp_json = wSJsonUtils.transfer2json(message)
    print(temp_json)
    import json
    json_loads = json.loads(temp_json)
    print(json_loads)
    print(json_loads["message_consumer_state_list"])
