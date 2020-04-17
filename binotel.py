from time import localtime, strftime
import websockets
import asyncio
import json
url = "wss://ws.binotel.com:9001"#url и keyss - присылают с Бинотела по запросу
keyss = {"task":"authLikeService","key":"0000000 ","secret":"000000000000000"}# - авторизация. есть и другие команды у них, но сначала нужно авторизоваться
		
async def binotel(): 
	async with websockets.connect(url) as websocket:
		await websocket.send(json.dumps(keyss))
		result = await websocket.recv()	
		#присылают текстом, что вы успешно вошли! Потом только ЖСоны будут слать	
		while True:#и цикл на постоянную прослушку сокета
			result = await websocket.recv()
			try:
				result = json.loads(result)
				result.setdefault("eventName",0)
			except:#иногда стринги приходят не нужные
				print(strftime('%Y.%m.%d %H:%M:%S',localtime()),"Ошибка: неформатный ответ от бинотела: ",result)
				continue

			#print(result)
			#присылаю при начале звонка
			#{'eventName': 'callStart', 'companyID': 0000, 'generalCallID': '000000', 'startTime': 1586974300, 'externalNumber': '77470000000', 
			#'callType': 0, 'customerName': '', 'customerDescription': '', 'pbxNumber': '77750000000', 
			#'linkToCrmUrl': 'https://my.binotel.ua/?module=addClient&number=77470000000', 'linkToCrmTitle': 'Создать контакт', 
			#'linkToCrm2Url': '', 'linkToCrm2Title': '', 'assignedToEmployeeName': '', 'bitrix24RegisteredCallId': '', 'internalNumbers': [], 
			#'pbxNumberName': '', 'isNewCall': 1}

			#присылаю при ответе на звонок
			#{"eventName":"callAnswer","generalCallID":"423695389","answeredAt":1509628018,"internalNumber":"737","externalNumber":"0673843136",
			#"callType":1,"customerName":"","customerDescription":"","linkToCrmUrl":"https://my.binotel.ua","linkToCrmTitle":"Создать контакт",
			#"linkToCrm2Url":"","linkToCrm2Title":"","assignedToEmployeeName":""}

			#присылаю при окончании звонка
			#{'eventName': 'callStop', 'generalCallID': '000000', 'stopTime': 1586974400, 'billsec': 100, 'disposition': 'VM-SUCCESS'}

			if result['eventName'] == "callStart" and result['callType'] == 1:
				print(strftime('%Y.%m.%d %H:%M:%S',localtime()),"Начался исходящий звонок на номер",result["externalNumber"])							

			if result['eventName'] == "callStart" and result['callType'] == 0:
				print(strftime('%Y.%m.%d %H:%M:%S',localtime()),"Начался входящий звонок с номера",result["externalNumber"])						

asyncio.get_event_loop().run_until_complete(binotel())
