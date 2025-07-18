# this is an example of the Uber API
# as a demonstration of an API spec in YAML
swagger: '2.0'
info:
  title: 中央氣象署開放資料平臺之資料擷取API
  description: 提供目前開放資料之擷取API
  version: "1.0.0"
# the domain of the service
# host: opendata.cwa.gov.tw
# array of all schemes that your API supports
schemes:
  - https
  - http
# will be prefixed to all paths
basePath: /api
produces:
  - application/json
  - application/xml
paths:
  /v1/rest/datastore/F-C0032-001:
    get:
      summary: 一般天氣預報-今明 36 小時天氣預報
      description: |
        臺灣各縣市天氣預報資料及國際都市天氣預報
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: locationName
          in: query
          description: 臺灣各縣市，預設為回傳全部縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: elementName
          in: query
          description: 天氣因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Wx
              - PoP
              - CI
              - MinT
              - MaxT

        - name: sort
          in: query
          description: 同時對 「startTime」，「endTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: startTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「startTime」，則參數「timeFrom」的篩選資料則會失去作用， 預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，根據內容可篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「startTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK


  /v1/rest/datastore/F-D0047-001:
    get:
      summary: 鄉鎮天氣預報-宜蘭縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度

        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK



  /v1/rest/datastore/F-D0047-003:
    get:
      summary: 鄉鎮天氣預報-宜蘭縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-005:
    get:
      summary: 鄉鎮天氣預報-桃園市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-007:
    get:
      summary: 鄉鎮天氣預報-桃園市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-009:
    get:
      summary: 鄉鎮天氣預報-新竹縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-011:
    get:
      summary: 鄉鎮天氣預報-新竹縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-013:
    get:
      summary: 鄉鎮天氣預報-苗栗縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-015:
    get:
      summary: 鄉鎮天氣預報-苗栗縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-017:
    get:
      summary: 鄉鎮天氣預報-彰化縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-019:
    get:
      summary: 鄉鎮天氣預報-彰化縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-021:
    get:
      summary: 鄉鎮天氣預報-南投縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-023:
    get:
      summary: 鄉鎮天氣預報-南投縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK


  /v1/rest/datastore/F-D0047-025:
    get:
      summary: 鄉鎮天氣預報-雲林縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-027:
    get:
      summary: 鄉鎮天氣預報-雲林縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-029:
    get:
      summary: 鄉鎮天氣預報-嘉義縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-031:
    get:
      summary: 鄉鎮天氣預報-嘉義縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-033:
    get:
      summary: 鄉鎮天氣預報-屏東縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-035:
    get:
      summary: 鄉鎮天氣預報-屏東縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-037:
    get:
      summary: 鄉鎮天氣預報-臺東縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-039:
    get:
      summary: 鄉鎮天氣預報-臺東縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-041:
    get:
      summary: 鄉鎮天氣預報-花蓮縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-043:
    get:
      summary: 鄉鎮天氣預報-花蓮縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK


  /v1/rest/datastore/F-D0047-045:
    get:
      summary: 鄉鎮天氣預報-澎湖縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-047:
    get:
      summary: 鄉鎮天氣預報-澎湖縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-049:
    get:
      summary: 鄉鎮天氣預報-基隆市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-051:
    get:
      summary: 鄉鎮天氣預報-基隆市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-053:
    get:
      summary: 鄉鎮天氣預報-新竹市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-055:
    get:
      summary: 鄉鎮天氣預報-新竹市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-057:
    get:
      summary: 鄉鎮天氣預報-嘉義市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-059:
    get:
      summary: 鄉鎮天氣預報-嘉義市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-061:
    get:
      summary: 鄉鎮天氣預報-臺北市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-063:
    get:
      summary: 鄉鎮天氣預報-臺北市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - - 最高溫度
                - 天氣預報綜合描述
                - 平均相對濕度
                - 最高體感溫度
                - 降雨機率
                - 風向
                - 平均露點溫度
                - 最低體感溫度
                - 平均溫度
                - 最大舒適度指數
                - 最小舒適度指數
                - 風速
                - 紫外線指數
                - 天氣現象
                - 最低溫度

        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK


  /v1/rest/datastore/F-D0047-065:
    get:
      summary: 鄉鎮天氣預報-高雄市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-067:
    get:
      summary: 鄉鎮天氣預報-高雄市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-069:
    get:
      summary: 鄉鎮天氣預報-新北市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-071:
    get:
      summary: 鄉鎮天氣預報-新北市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-073:
    get:
      summary: 鄉鎮天氣預報-臺中市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-075:
    get:
      summary: 鄉鎮天氣預報-臺中市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-077:
    get:
      summary: 鄉鎮天氣預報-臺南市未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-079:
    get:
      summary: 鄉鎮天氣預報-臺南市未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-081:
    get:
      summary: 鄉鎮天氣預報-連江縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-083:
    get:
      summary: 鄉鎮天氣預報-連江縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-085:
    get:
      summary: 鄉鎮天氣預報-金門縣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK
  /v1/rest/datastore/F-D0047-087:
    get:
      summary: 鄉鎮天氣預報-金門縣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)及未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段:時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo 合併使用，格式為「yyyy-MM-ddThh:mm:ss」， 若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK


  ########################################

  /v1/rest/datastore/F-D0047-089:
    get:
      summary: 鄉鎮天氣預報-臺灣未來3天天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來3天(逐3小時)
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 臺灣各縣市，預設為回傳全部縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 「timeTo」，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-091:
    get:
      summary: 鄉鎮天氣預報-臺灣未來1週天氣預報
      description: |
        臺灣各鄉鎮市區預報資料-臺灣各鄉鎮市區未來1週天氣預報
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 臺灣各縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: ElementName
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 最高溫度
              - 天氣預報綜合描述
              - 平均相對濕度
              - 最高體感溫度
              - 降雨機率
              - 風向
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 風速
              - 紫外線指數
              - 天氣現象
              - 最低溫度

        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-D0047-093:
    get:
      summary: 鄉鎮天氣預報-全臺灣各鄉鎮市區預報資料
      description: |
        鄉鎮天氣預報可跨縣市截取單一鄉鎮市區預報資料
        因應系統負載最多一次可擷取5個指定縣市之單一鄉鎮市區預報資料，最少1個指定縣市之單一鄉鎮市區預報資料。

      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int
        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: locationId
          in: query
          description: 單一鄉鎮市區預報資料之資料項編號:F-D0047-001至F-D0047-091(單號)，最多五個欄位，最少一個欄位
          required: true
          type: array
          items:
            type: string
            minItems: 1
            maxItems: 5
            enum:
              - F-D0047-001
              - F-D0047-003
              - F-D0047-005
              - F-D0047-007
              - F-D0047-009
              - F-D0047-011
              - F-D0047-013
              - F-D0047-015
              - F-D0047-017
              - F-D0047-019
              - F-D0047-021
              - F-D0047-023
              - F-D0047-025
              - F-D0047-027
              - F-D0047-029
              - F-D0047-031
              - F-D0047-033
              - F-D0047-035
              - F-D0047-037
              - F-D0047-039
              - F-D0047-041
              - F-D0047-043
              - F-D0047-045
              - F-D0047-047
              - F-D0047-049
              - F-D0047-051
              - F-D0047-053
              - F-D0047-055
              - F-D0047-057
              - F-D0047-059
              - F-D0047-061
              - F-D0047-063
              - F-D0047-065
              - F-D0047-067
              - F-D0047-069
              - F-D0047-071
              - F-D0047-073
              - F-D0047-075
              - F-D0047-077
              - F-D0047-079
              - F-D0047-081
              - F-D0047-083
              - F-D0047-085
              - F-D0047-087
              - F-D0047-089
              - F-D0047-091

        - name: LocationName
          in: query
          description: 各縣市所對應鄉鎮名稱，請詳 https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf 附錄 A『全臺縣市鄉鎮對照表』
          required: false
          type: array
          items:
            type: string

        - name: ElementName
          in: query
          description: 天氣預報天氣因子，可以接受3天天氣預報天氣因子及1週天氣預報天氣因子。預設為所輸入各個locationId 對應的所有欄位。
          required: false
          type: array
          items:
            type: string
            enum:
              - 露點溫度
              - 天氣預報綜合描述
              - 舒適度指數
              - 風向
              - 降雨機率
              - 溫度
              - 風速
              - 天氣現象
              - 相對濕度
              - 體感溫度
              - 最高溫度
              - 平均相對濕度
              - 最高體感溫度
              - 平均露點溫度
              - 最低體感溫度
              - 平均溫度
              - 最大舒適度指數
              - 最小舒適度指數
              - 紫外線指數
              - 最低溫度

        - name: sort
          in: query
          description: 同時對 「StartTime」，「EndTime」，「DataTime」 做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - time

        - name: StartTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「StartTime」或「DataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-A0021-001:
    get:
      summary: 潮汐預報-未來 1 個月潮汐預報
      description: |
        未來1個月潮汐預報
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: LocationName
          in: query
          description: 地點，請參考https://opendata.cwa.gov.tw/opendatadoc/Forecast/F-A0021-001.pdf，若使用參數「LocationId」，則參數「LocationName」的篩選會失效，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: LocationId
          in: query
          description: 地點，請參考https://opendata.cwa.gov.tw/opendatadoc/Forecast/F-A0021-001.pdf，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: WeatherElement
          in: query
          description: 氣象因子，預設為全部回傳；若未選擇Tide或TideHeight，Time就不顯示
          required: false
          type: array
          items:
            type: string
            enum:
              - LunarDate
              - TideRange
              - Tide
              - TideHeights

        - name: TideRange
          in: query
          description: 潮差，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 大
              - 中
              - 小

        - name: sort
          in: query
          description: 「Date」 為針對「Date」做排序，「DateTime」 為針對 「DateTime」 做排序，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - Date
              - DateTime

        - name: Date
          in: query
          description: 預報時間因子，日期，格式為「yyyy-MM-dd」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}$'

        - name: hhmmss
          in: query
          description: 潮汐時間因子，格式為「hh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: time
            pattern: '^\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數「timeTo」合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「Date」或「hhmmss」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「Date」或「hhmmss」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
      tags:
        - 預報
      responses:
        200:
          description: OK


  /v1/rest/datastore/F-A0085-002:
    get:
      summary: 健康氣象冷傷害指數及警示全臺各鄉鎮五日預報
      description: |
        健康氣象相關預報資料-冷傷害指數及警示全臺各鄉鎮五日預報
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 各縣市名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: TownName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: WeatherElements
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - ColdInjuryIndex
              - ColdInjuryWarning

        - name: StartTime
          in: query
          description:
            時間因子，預設全部回傳，格式為「yyyy-MM-ddThh:mm:ss」
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: sort
          in: query
          description: 「StartTime」 為針對「StartTime」，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - StartTime

      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-A0085-003:
    get:
      summary: 健康氣象冷傷害指數及警示全臺各鄉鎮未來72小時逐3小時預報
      description: |
        健康氣象相關數值預報資料-熱傷害分級與綜合溫度熱指數
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 各縣市名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: TownName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: WeatherElements
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - ColdInjuryIndex
              - ColdInjuryWarning

        - name: IssueTime
          in: query
          description:
            時間因子，預設全部回傳，格式為「yyyy-MM-ddThh:mm:ss」
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用「IssueTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: sort
          in: query
          description: 「IssueTime」 為針對「IssueTime」，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - IssueTime

      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-A0085-004:
    get:
      summary: 健康氣象溫差提醒指數及警示全臺各鄉鎮五日預報
      description: |
        健康氣象相關預報資料-健康氣象溫差提醒指數及警示全臺各鄉鎮五日預報
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 各縣市名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: TownName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: WeatherElements
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - MaxTemperature
              - MinTemperature
              - TemperatureDifferenceWarning

        - name: StartTime
          in: query
          description:
            時間因子，預設全部回傳，格式為「yyyy-MM-ddThh:mm:ss」
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用參數「StartTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用「StartTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: sort
          in: query
          description: 「StartTime」 為針對「StartTime」做排序，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - StartTime

      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/F-A0085-005:
    get:
      summary: 健康氣象溫差提醒指數及警示全臺各鄉鎮未來72小時逐3小時預報
      description: |
        健康氣象相關數值預報資料-健康氣象溫差提醒指數及警示全臺各鄉鎮未來72小時逐3小時預報
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 各縣市名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: TownName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: WeatherElements
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - TemperatureDifferenceIndex
              - TemperatureDifferenceWarning

        - name: IssueTime
          in: query
          description:
            時間因子，預設全部回傳，格式為「yyyy-MM-ddThh:mm:ss」
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用「IssueTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: sort
          in: query
          description: 「IssueTime」 為針對「IssueTime做排序」，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - IssueTime

      tags:
        - 預報
      responses:
        200:
          description: OK

  /v1/rest/datastore/O-A0001-001:
    get:
      summary: 自動氣象站-氣象觀測資料
      description: |
        自動氣象站資料-無人自動站氣象資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationId
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，可輸入多個站號，大小寫必須完全符合，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: StationName
          in: query
          description: 測站站名，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，可輸入多個站名，預設為全部回傳，若使用「StationId」，則參數「StationName」的篩選資料則會失效，只會回傳StationId符合的資料
          required: false
          type: array
          items:
            type: string

        - name: WeatherElement
          in: query
          description: 氣象因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Weather
              - Now
              - WindDirection
              - WindSpeed
              - AirTemperature
              - RelativeHumidity
              - AirPressure
              - GustInfo
              - DailyHigh
              - DailyLow

        - name: GeoInfo
          in: query
          description: 參數，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Coordinates
              - StationAltitude
              - CountyName
              - TownName
              - CountyCode
              - TownCode

      tags:
        - 觀測
      responses:
        200:
          description: OK


  /v1/rest/datastore/O-A0002-001:
    get:
      summary: 自動雨量站-雨量觀測資料
      description: |
        自動雨量站資料-無人自動站雨量資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationId
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，可輸入多個站號，大小寫必須完全符合，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: StationName
          in: query
          description: 測站站名，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，可輸入多個站名，預設為全部回傳，若使用「StationId」，則參數「StationName」的篩選資料則會失效，只會回傳StationId符合的資料
          required: false
          type: array
          items:
            type: string

        - name: RainfallElement
          in: query
          description: 氣象因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Now
              - Past10Min
              - Past1hr
              - Past3hr
              - Past6hr
              - Past12hr
              - Past24hr
              - Past2days
              - Past3days

        - name: GeoInfo
          in: query
          description: 參數，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Coordinates
              - StationAltitude
              - CountyName
              - TownName
              - CountyCode
              - TownCode

      tags:
        - 觀測
      responses:
        200:
          description: OK


  /v1/rest/datastore/O-A0003-001:
    get:
      summary: 現在天氣觀測報告-現在天氣觀測報告
      description: |
        現在天氣觀測報告-有人氣象站資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationId
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，可輸入多個站號，大小寫必須完全符合，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: StationName
          in: query
          description: 測站站名，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，可輸入多個站名，預設為全部回傳，若使用「StationId」，則參數「StationName」的篩選資料則會失效，只會回傳StationId符合的資料
          required: false
          type: array
          items:
            type: string

        - name: WeatherElement
          in: query
          description: 氣象因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Weather
              - VisibilityDescription
              - SunshineDuration
              - Now
              - WindDirection
              - WindSpeed
              - AirTemperature
              - RelativeHumidity
              - AirPressure
              - UVIndex
              - Max10MinAverage
              - GustInfo
              - DailyHigh
              - DailyLow

        - name: GeoInfo
          in: query
          description: 參數，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - Coordinates
              - StationAltitude
              - CountyName
              - TownName
              - CountyCode
              - TownCode

      tags:
        - 觀測
      responses:
        200:
          description: OK


  /v1/rest/datastore/O-A0005-001:
    get:
      summary: 紫外線指數-每日紫外線指數最大值
      description: |
        氣象站每日紫外線指數最大值-每天下午2時左右會提供各站紫外線的當日最大值
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，預設為全部回傳
          required: false
          type: array
          items:
            type: string

      tags:
        - 觀測
      responses:
        200:
          description: OK



  /v1/rest/datastore/O-A0006-002:
    get:
      summary: 臭氧總量觀測資料-台北站
      description: |
        臭氧總量觀測資料-臭氧總量觀測資料(台北)
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: elementName
          in: query
          description: 臭氧量統計因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 累年臭氧全量累年平均值
              - 累年臭氧全量累年月平均值最低
              - 累年臭氧全量月平均值
              - 累年臭氧全量累年月平均值
              - 累年臭氧全量累年月平均值最高


        - name: dataTime
          in: query
          description: 時間因子，格式有 「yyyy」，「MM」，「yyyyy-MM」，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 進行時間升冪排序，預設不排序
          required: false
          type: string
          enum:
            - dataTime

      tags:
        - 觀測
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/O-B0075-001:
    get:
      summary: 海象監測資料-48小時浮標站與潮位站海況監測資料
      description: |
        海象監測資料-48小時浮標站與潮位站海況監測資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站代碼，請參考https://opendata.cwa.gov.tw/dataset/observation/O-B0076-001
          required: false
          type: array
          items:
            type: string

        - name: WeatherElement
          in: query
          description: 氣象因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - TideHeight
              - TideLevel
              - WaveHeight
              - WaveDirection
              - WaveDirectionDescription
              - WavePeriod
              - SeaTemperature
              - Temperature
              - StationPressure
              - PrimaryAnemometer
              - SeaCurrents
        - name: sort
          in: query
          description: 針對 「StationID」或「DataTime」做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - StationID
            - DataTime

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」。 若使用參數「DataTime」，則參數「timeFrom」的篩選資料則會失效。預設全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」。 若使用「DataTime」，則參數「timeTo」的篩選資料則會失效。預設全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

      tags:
        - 觀測
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/O-B0075-002:
    get:
      summary: 海象監測資料-30天浮標站與潮位站海況監測資料
      description: |
        海象監測資料-30天浮標站與潮位站海況監測資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站代碼，請參考https://opendata.cwa.gov.tw/dataset/observation/O-B0076-001
          required: false
          type: array
          items:
            type: string

        - name: WeatherElement
          in: query
          description: 氣象因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - TideHeight
              - TideLevel
              - WaveHeight
              - WaveDirection
              - WaveDirectionDescription
              - WavePeriod
              - SeaTemperature
              - Temperature
              - StationPressure
              - PrimaryAnemometer
              - SeaCurrents
        - name: sort
          in: query
          description: 針對 「StationID」或「DataTime」做升冪排序，預設不排序
          required: false
          type: string
          enum:
            - StationID
            - DataTime

        - name: DataTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，最多回傳24個小時的資料。預設回傳最早24個小時的資料。
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
          maxItems: 24

        - name: timeFrom
          in: query
          description: |
            時間區段，篩選需要之時間區段，格式為「yyyy-MM-ddThh:mm:ss」

            時間從「timeFrom」開始篩選，直到「timeFrom」之後24小時的資料
            並可與參數 「timeTo」 合併使用，時間從「timeFrom」開始篩選，直到「timeTo」，可回傳最多24小時長度的資料
            在合併使用參數「timeTo」和參數「timeFrom」的時候，若是 「timeTo」的時間超過「timeFrom」之後24小時，則僅會回傳「timeFrom」開始後24小時之間的資料

            若使用參數「DataTime」，則參數「timeFrom」的篩選資料則會失效
            若是參數「timeFrom」和參數「timeTo」都沒有設定，預設會回傳內容中最初24小時的資料
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: |
            時間區段，篩選需要之時間區段，格式為「yyyy-MM-ddThh:mm:ss」

            時間從「timeTo」之前24小時開始篩選，直到「timeTo」
            並可與參數 「timeFrom」 合併使用，時間從「timeFrom」開始篩選，直到「timeTo」，可回傳最多24小時長度的資料
            在合併使用參數「timeTo」和參數「timeFrom」的時候，若是 「timeTo」的時間超過「timeFrom」之後24小時，則僅會回傳「timeFrom」開始後24小時之間的資料

            若使用參數「DataTime」，則參數「timeTo」的篩選資料則會失效
            若是參數「timeFrom」和參數「timeTo」都沒有設定，預設會回傳內容中最初24小時的資料
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

      tags:
        - 觀測
      responses:
        200:
          description: OK

  ##################
  /v1/rest/datastore/E-A0014-001:
    get:
      summary: 海嘯資訊資料-海嘯資訊資料
      description: |
        海嘯資訊資料
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: AreaName
          in: query
          description: 區域名稱 ，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: StationName
          in: query
          description: 測站名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 「OriginTime」為針對「OriginTime」與「ReportNo」做升冪排序，預設「OriginTime」與「ReportNo」為降冪排序
          required: false
          type: array
          items:
            type: string
            enum:
              - OriginTime

        - name: OriginTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            format: date-time
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效 ，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數 timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「dataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 地震海嘯
      responses:
        200:
          description: OK
  ###############################
  /v1/rest/datastore/E-A0015-001:
    get:
      summary: 顯著有感地震報告資料-顯著有感地震報告
      description: |
        顯著有感地震報告
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: AreaName
          in: query
          description: 臺灣各縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: StationName
          in: query
          description: 測站名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 設為「OriginTime」為針對時間因子做升冪排序，預設為降冪排序
          required: false
          type: string
          items:
            type: string
            enum:
              - OriginTime

        - name: OriginTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效 ，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數 timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「dataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 地震海嘯
      responses:
        200:
          description: OK


  ###############################
  /v1/rest/datastore/E-A0015-002:
    get:
      summary: 顯著有感地震報告資料-顯著有感地震報告(英文)
      description: |
        提供顯著有感地震報告資料-英文版地震報告
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: AreaName
          in: query
          description: 臺灣各縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - Yilan County
              - Hualien County
              - Taitung County
              - Penghu County
              - Kinmen County
              - Lienchiang County
              - Taipei City
              - New Taipei City
              - Taoyuan City
              - Taichung City
              - Tainan City
              - Kaohsiung City
              - Keelung City
              - Hsinchu County
              - Hsinchu City
              - Miaoli County
              - Changhua County
              - Nantou County
              - Yunlin County
              - Chiayi County
              - Chiayi City
              - Pingtung County

        - name: StationName
          in: query
          description: 測站名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 設為「OriginTime」為針對時間因子做升冪排序，預設為降冪排序
          required: false
          type: string
          items:
            type: string
            enum:
              - OriginTime

        - name: OriginTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效 ，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數 timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「dataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 地震海嘯
      responses:
        200:
          description: OK

  ###############################
  /v1/rest/datastore/E-A0016-001:
    get:
      summary: 小區域有感地震報告資料-小區域有感地震報告
      description: |
        小區域有感地震報告
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string
        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int
        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML
        - name: AreaName
          in: query
          description: 臺灣各縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: StationName
          in: query
          description: 測站名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 設為「OriginTime」為針對時間因子做升冪排序，預設為降冪排序
          required: false
          type: string
          items:
            type: string
            enum:
              - OriginTime

        - name: OriginTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效 ，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數 timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「dataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 地震海嘯
      responses:
        200:
          description: OK

  ###############################
  /v1/rest/datastore/E-A0016-002:
    get:
      summary: 小區域有感地震報告資料-小區域有感地震報告(英文)
      description: |
        提供小區域有感地震報告資料-英文版地震報告
      parameters:
        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string
        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int
        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML
        - name: AreaName
          in: query
          description: 臺灣各縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - Yilan County
              - Hualien County
              - Taitung County
              - Penghu County
              - Kinmen County
              - Lienchiang County
              - Taipei City
              - New Taipei City
              - Taoyuan City
              - Taichung City
              - Tainan City
              - Kaohsiung City
              - Keelung City
              - Hsinchu County
              - Hsinchu City
              - Miaoli County
              - Changhua County
              - Nantou County
              - Yunlin County
              - Chiayi County
              - Chiayi City
              - Pingtung County

        - name: StationName
          in: query
          description: 測站名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 設為「OriginTime」為針對時間因子做升冪排序，預設為降冪排序
          required: false
          type: string
          items:
            type: string
            enum:
              - OriginTime

        - name: OriginTime
          in: query
          description: 時間因子，格式為「yyyy-MM-ddThh:mm:ss」，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效 ，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數 timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」，若使用「dataTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
      tags:
        - 地震海嘯
      responses:
        200:
          description: OK


  #########################
  /v1/rest/datastore/C-B0025-001:
    get:
      summary: 每日雨量-地面測站每日雨量資料
      description: |
        地面測站每日雨量資料-每日雨量
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: sort
          in: query
          description: 「time」 為針對月份因子做升冪排序，「dataTime」為針對時間因子做升冪排序，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - dataTime

        - name: Date
          in: query
          description: 時間因子，格式為 「yyyy-MM-dd」，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: timeFrom
          in: query
          description: 時間區段，篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-dd」，若使用參數「Date」，則參數「timeFrom」的篩選資料則會失效 ，預設為全部回傳
          required: false
          type: string
          format: date-time

        - name: timeTo
          in: query
          description: 時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數 timeFrom」 合併使用，格式為「yyyy-MM-dd」，若使用「Date」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date-time

        - name: statistics
          in: query
          description: 是否選取每月雨量統計值，若選取的話則只回傳統計值，並且參數「Date」，參數「timeTo」，參數「timeFrom」失效。 預設為false
          required: false
          type: boolean

      tags:
        - 氣候
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/C-B0027-001:
    get:
      summary: 月平均-地面測站資料
      description: |
        月平均-地面測站資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: weatherElement
          in: query
          description: 要查詢的天氣要素
          required: false
          type: array
          items:
            type: string
            enum:
              - AirPressure
              - AirTemperature
              - RelativeHumidity
              - CloudAmount
              - SunshineDuration
              - Precipitation
              - WindSpeed

        - name: Month
          in: query
          description: 要查詢的月份，查詢1回傳1月份資料，查詢2回傳2月份資料，依此類推
          required: false
          type: array
          items:
            type: integer
            enum:
              - 1
              - 2
              - 3
              - 4
              - 5
              - 6
              - 7
              - 8
              - 9
              - 10
              - 11
              - 12

      tags:
        - 氣候
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/C-B0074-001:
    get:
      summary: 氣象測站基本資料-有人氣象測站基本資料
      description: |
        氣象測站基本資料-有人氣象測站基本資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: status
          in: query
          description: 測站狀態
          required: false
          type: array
          items:
            type: string
            enum:
              - 現存測站
              - 已撤銷
      tags:
        - 氣候
      responses:
        200:
          description: OK
  #########################
  /v1/rest/datastore/C-B0074-002:
    get:
      summary: 氣象測站基本資料-無人氣象測站基本資料
      description: |
        氣象測站基本資料-無人氣象測站基本資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: StationID
          in: query
          description: 測站站號，請參考https://e-service.cwa.gov.tw/wdps/obs/state.htm ，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: status
          in: query
          description: 測站狀態
          required: false
          type: array
          items:
            type: string
            enum:
              - 現存測站
              - 已撤銷
      tags:
        - 氣候
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/W-C0033-001:
    get:
      summary: 天氣特報-各別縣市地區目前之天氣警特報情形
      description: |
        天氣特報-各別縣市地區目前之天氣警特報情形
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML
        - name: locationName
          in: query
          description: 縣市名稱，預設為所有縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: phenomena
          in: query
          description: 當時發佈之警特報類型
          required: false
          type: array
          items:
            type: string
            enum:
              - 濃霧
              - 大雨
              - 豪雨
              - 大豪雨
              - 超大豪雨
              - 陸上強風
              - 海上陸上颱風

      tags:
        - 天氣警特報
      responses:
        200:
          description: OK
  #########################
  /v1/rest/datastore/W-C0033-002:
    get:
      summary: 天氣特報-各別天氣警特報之內容及所影響之區域
      description: |
        天氣特報-各別天氣警特報之內容及所影響之區域
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML
        - name: locationName
          in: query
          description: 依照當時發佈特報之涵蓋區域市，區域名稱請詳見 https://opendata.cwa.gov.tw/opendatadoc/Opendata_Warnings.pdf 附錄 B『特報之影響區域名稱對照表』
          required: false
          type: array
          items:
            type: string

        - name: phenomena
          in: query
          description: 當時發佈之警特報類型
          required: false
          type: array
          items:
            type: string
            enum:
              - 濃霧
              - 大雨
              - 豪雨
              - 大豪雨
              - 超大豪雨
              - 陸上強風
              - 颱風

      tags:
        - 天氣警特報
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/W-C0034-005:
    get:
      summary: 颱風消息與警報-熱帶氣旋路徑
      description: |
        西北太平洋地區及南海目前所有活動中熱帶氣旋之資訊-熱帶性低氣壓及颱風過去、現在及未來預報之資訊
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料，預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳，預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式，預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML
        - name: cwaTdNo
          in: query
          description: 為熱帶性低氣壓編號，預設全部回傳
          required: false
          type: number
          format: int

        - name: dataset
          in: query
          description: analysisData/forecastData，預設全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - analysisData
              - forecastData

        - name: fixTime
          in: query
          description:
            過去及現在定位時間，預設全部回傳, 格式為「yyyy-MM-ddThh:mm:ss」
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: tau
          in: query
          description: 預報時距，預設全部回傳 輸入數字6~120 可輸入多筆資料，用逗號分隔
          required: false
          type: array
          items:
            type: number
            format: int

        - name: timeFrom
          in: query
          description:
            時間區段，針對analysisData篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用

            格式為「yyyy-MM-ddThh:mm:ss」，若使用參數「fix_time」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description:
            時間區段，針對analysisData篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用

            格式為「yyyy-MM-ddThh:mm:ss」，若使用「fix_time」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: sort
          in: query
          description: 對「cwaTdNo」進行升冪排序, 預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - cwaTdNo

      tags:
        - 天氣警特報
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/M-A0085-001:
    get:
      summary: 健康氣象-熱傷害指數及警示全台各鄉鎮五日逐三小時預報
      description: |
        健康氣象相關數值預報資料-熱傷害分級與綜合溫度熱指數
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 各縣市名稱，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: TownName
          in: query
          description: 各縣市所對應鄉鎮名稱，請參考https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf ，附錄 A『全臺縣市鄉鎮對照表』，預設為全部回傳
          required: false
          type: array
          items:
            type: string

        - name: WeatherElements
          in: query
          description: 天氣預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - HeatInjuryIndex
              - HeatInjuryWarning

        - name: IssueTime
          in: query
          description:
            時間因子，預設全部回傳，格式為「yyyy-MM-ddThh:mm:ss」
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeFrom
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從「timeFrom」 開始篩選，直到內容之最後時間，並可與參數 「timeTo」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用參數「dataTime」，則參數「timeFrom」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: timeTo
          in: query
          description:
            時間區段，篩選需要之時間區段，時間從內容之最初時間開始篩選，直到 timeTo，並可與參數 「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

            若使用「IssueTime」，則參數「timeTo」的篩選資料則會失效，預設為全部回傳
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

        - name: sort
          in: query
          description: 「IssueTime」 為針對「IssueTime」，預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - IssueTime

      tags:
        - 數值預報
      responses:
        200:
          description: OK

  #########################
  /v1/rest/datastore/A-B0062-001:
    get:
      summary: 日出日沒時刻-全臺各縣市年度逐日日出日沒時刻資料
      description: |
        全臺各縣市每天的日出、日沒及太陽過中天等時刻資料
        含有日出日沒時之方位及過中天時之仰角資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 臺灣各縣市, 預設為回傳全部縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: Date
          in: query
          description:  |
            時間因子, 格式為「yyyy-MM-dd」, 最多回傳180筆資料
            預設回傳內容之最初180筆的資料
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}$'
          maxItems: 180

        - name: parameter
          in: query
          description: 預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - BeginCivilTwilightTime
              - SunRiseTime
              - SunRiseAZ
              - SunTransitTime
              - SunTransitAlt
              - SunSetTime
              - SunSetAZ
              - EndCivilTwilightTime

        - name: timeFrom
          in: query
          description: |
            時間區段,篩選需要之時間區段,格式為「yyyy-MM-dd」

            時間從「timeFrom」開始篩選,直到「timeFrom」之後180天的資料
            可與參數 「timeTo」 合併使用,時間從「timeFrom」開始篩選,直到「timeTo」,可回傳最多180天長度的資料
            在合併使用參數「timeTo」和參數「timeFrom」的時候，若是 「timeTo」的時間超過「timeFrom」之後180天，則僅會回傳「timeFrom」開始直到「timeFrom」之後180天之間的資料

            若使用參數「Date」,則參數「timeFrom」的篩選資料則會失效

            若是參數「timeFrom」和參數「timeTo」都沒有設定，預設會回傳內容中最初180筆的資料
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}$'

        - name: timeTo
          in: query
          description:  |
            時間區段, 篩選需要之時間區段,格式為「yyyy-MM-dd」

            時間從「timeTo」之前180天開始篩選,直到「timeTo」
            可與參數「 timeFrom」 合併使用,時間從「timeFrom」開始篩選,直到「timeTo」,可回傳最多180天長度的資料
            在合併使用參數「timeTo」和參數「timeFrom」的時,若是 「timeTo」的時間超過「timeFrom」之後180天,則僅會回傳「timeFrom」開始直到「timeFrom」之後180天之間的資料

            若使用參數「Date」,則參數「timeTo」的篩選資料則會失效

            若是參數「timeFrom」和參數「timeTo」都沒有設定,預設會回傳內容中最初180筆的資料
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}$'

        - name: sort
          in: query
          description: 對「CountyName」或「Date」進行升冪排序, 預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - CountyName
              - Date

      tags:
        - 天文
      responses:
        200:
          description: OK
    #########################
  /v1/rest/datastore/A-B0063-001:
    get:
      summary: 月出月沒時刻-全臺各縣市年度逐日月出月沒時刻資料
      description: |
        全臺各縣市每天的月出、月沒及月球過中天等時刻資料
        含有月出月沒時之方位及過中天時之仰角資料
      parameters:

        - name: Authorization
          in: query
          description: 氣象開放資料平台會員授權碼
          required: true
          type: string

        - name: limit
          in: query
          description: 限制最多回傳的資料, 預設為回傳全部筆數
          required: false
          type: number
          format: int

        - name: offset
          in: query
          description: 指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳
          required: false
          type: number
          format: int

        - name: format
          in: query
          description: 回傳資料格式, 預設為 json 格式
          required: false
          type: string
          enum:
            - JSON
            - XML

        - name: CountyName
          in: query
          description: 臺灣各縣市, 預設為回傳全部縣市
          required: false
          type: array
          items:
            type: string
            enum:
              - 宜蘭縣
              - 花蓮縣
              - 臺東縣
              - 澎湖縣
              - 金門縣
              - 連江縣
              - 臺北市
              - 新北市
              - 桃園市
              - 臺中市
              - 臺南市
              - 高雄市
              - 基隆市
              - 新竹縣
              - 新竹市
              - 苗栗縣
              - 彰化縣
              - 南投縣
              - 雲林縣
              - 嘉義縣
              - 嘉義市
              - 屏東縣

        - name: Date
          in: query
          description: |
            時間因子, 格式為「yyyy-MM-dd」, 最多回傳180筆資料
            預設回傳內容之最初180筆的資料
          required: false
          type: array
          items:
            type: string
            format: date
            pattern: '^\d{4}-\d{2}-\d{2}$'
          maxItems: 180

        - name: parameter
          in: query
          description: 預報因子，預設為全部回傳
          required: false
          type: array
          items:
            type: string
            enum:
              - MoonRiseTime
              - MoonRiseAZ
              - MoonTransitTime
              - MoonTransitAlt
              - MoonSetTime
              - MoonSetAZ

        - name: timeFrom
          in: query
          description: |
            時間區段,篩選需要之時間區段,格式為「yyyy-MM-dd」

            時間從「timeFrom」開始篩選,直到「timeFrom」之後180天的資料
            並可與參數 「timeTo」 合併使用,時間從「timeFrom」開始篩選,直到「timeTo」,可回傳最多180天長度的資料
            在合併使用參數「timeTo」和參數「timeFrom」的時候,若是 「timeTo」的時間超過「timeFrom」之後180天,則僅會回傳「timeFrom」開始直到「timeFrom」之後180天之間的資料

            若使用參數「Date」,則參數「timeFrom」的篩選資料則會失效

            若是參數「timeFrom」和參數「timeTo」都沒有設,預設會回傳內容中最初180筆的資料
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}$'

        - name: timeTo
          in: query
          description: |
            時間區段, 篩選需要之時間區段,格式為「yyyy-MM-dd」

            時間從「timeTo」之前180天開始篩選,直到「timeTo」
            並可與參數 「timeFrom」 合併使用,時間從「timeFrom」開始篩選,直到「timeTo」,可回傳最多180天長度的資料
            在合併使用參數「timeTo」和參數「timeFrom」的時候,若是 「timeTo」的時間超過「timeFrom」之後180天,則僅會回傳「timeFrom」開始直到「timeFrom」之後180天之間的資料

            若使用參數「Date」,則參數「timeTo」的篩選資料則會失效

            若是參數「timeFrom」和參數「timeTo」都沒有設定,預設會回傳內容中最初180筆的資料
          required: false
          type: string
          format: date
          pattern: '^\d{4}-\d{2}-\d{2}$'

        - name: sort
          in: query
          description: 對「CountyName」或「Date」進行升冪排序, 預設不排序
          required: false
          type: array
          items:
            type: string
            enum:
              - CountyName
              - Date

      tags:
        - 天文
      responses:
        200:
          description: OK