#  file: api/views.py
import json
import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.serializers import StockListSerializer, StockInformationHistorySerializer, StockPriceHistorySerializer, HistoricalStockPriceSerializer, StockSummarySerializer, StockYearlyFinancialStatementsSerializer, StockQuarterlyFinancialStatementsSerializer, StockProfileSerializer
from api.models import StockList, StockInformationHistory, StockPriceHistory, StockProfile


class StockPageNumberPagination(PageNumberPagination):
    page_size = 10


class StockListListAPIView(ListAPIView):
    queryset = StockList.objects.all()
    serializer_class = StockListSerializer
    pagination_class = StockPageNumberPagination


class StockListRetrieveAPIView(RetrieveAPIView):
    queryset = StockList.objects.all()
    lookup_field = "ticker"
    serializer_class = StockListSerializer


class StockInformationHistoryListAPIView(ListAPIView):
    serializer_class = StockInformationHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])


class StockInformationSparkListAPIView(ListAPIView):
    serializer_class = StockInformationHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])\
            .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]])


class StockInformationHistoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = StockInformationHistorySerializer
    pagination_class = StockPageNumberPagination
    lookup_field = "update_date"

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class StockPriceHistoryListAPIView(ListAPIView):
    serializer_class = StockPriceHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])


class StockPriceSparkListAPIView(ListAPIView):
    serializer_class = StockPriceHistorySerializer
    pagination_class = StockPageNumberPagination

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])\
            .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]])


class StockPriceHistoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = StockPriceHistorySerializer
    pagination_class = StockPageNumberPagination
    lookup_field = "update_date"

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class HistoricalStockPriceAPIView(ListAPIView):
    serializer_class = HistoricalStockPriceSerializer

    def get_queryset(self):
        return StockPriceHistory.objects.filter(ticker=self.kwargs["ticker"])\
           .filter(update_date__range=[self.kwargs["s_date"], self.kwargs["e_date"]]).reverse()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return_dict = dict()
        return_dict["ticker"] = self.kwargs["ticker"]
        return_dict["dateArray"] = list()
        return_dict["closeArray"] = list()
        return_dict["openArray"] = list()
        return_dict["highArray"] = list()
        return_dict["lowArray"] = list()
        return_dict["volumeArray"] = list()

        for idx, item in enumerate(serializer.data):
            iter_dict = json.loads(json.dumps(item))
            return_dict["dateArray"].append(iter_dict["update_date"])
            return_dict["closeArray"].append(iter_dict["price_close"])
            return_dict["openArray"].append(iter_dict["price_open"])
            return_dict["highArray"].append(iter_dict["price_high"])
            return_dict["lowArray"].append(iter_dict["price_low"])
            return_dict["volumeArray"].append(iter_dict["volume"])

        return Response(return_dict)


class StockSummaryAPIView(RetrieveAPIView):
    queryset = StockList.objects.prefetch_related() 
    lookup_field="ticker"
    serializer_class = StockSummarySerializer
    
    def get(self, request, ticker):
        obj = self.get_object()
        print(obj)
        priceUnit = "dollar" if re.search("^NYSE|^Nasdaq", obj.market) else None

        return Response({
            'ticker': obj.ticker,
            'koreanName': obj.name_korea,
            'englishName': obj.name_english,
            'tagList': list(),
            'priceUnit': priceUnit,
            'currentPrice': f"{obj.price:.2f}" if (obj.price is not None) else None,
            'dailyChange': f"{obj.price - obj.price_open:.2f}" if (obj.price is not None) & (obj.price_open is not None) else None,
            'dailyChangePercentage': f"{(obj.price - obj.price_open)/obj.price_open:.2f}" if (obj.price is not None) & (obj.price_open is not None) else None,
            '52weekHigh': f"{obj.stockinformationhistory.fiftytwoweek_high:.2f}" if (obj.stockinformationhistory.fiftytwoweek_high is not None) else None,
            '52weekLow': f"{obj.stockinformationhistory.fiftytwoweek_low:.2f}" if (obj.stockinformationhistory.fiftytwoweek_low is not None) else None,
            "fallingPercentageFrom52WeekHigh": f"{(obj.stockinformationhistory.fiftytwoweek_high - obj.price) / obj.stockinformationhistory.fiftytwoweek_high:.2f}" if (obj.stockinformationhistory.fiftytwoweek_high is not None) else None,
            "ttmPER" : f"{obj.stockinformationhistory.ttmPER:.2f}" if (obj.stockinformationhistory.ttmPER is not None) else None,
            "ttmPSR" : f"{obj.stockinformationhistory.ttmPSR:.2f}" if (obj.stockinformationhistory.ttmPSR is not None) else None,
            "ttmPBR" : f"{obj.stockinformationhistory.ttmPBR:.2f}" if (obj.stockinformationhistory.ttmPBR is not None) else None,
            "ttmPEGR" : f"{obj.stockinformationhistory.ttmPEGR:.2f}" if (obj.stockinformationhistory.ttmPEGR is not None) else None,
            "forwardPER" : f"{obj.stockinformationhistory.forwardPER:.2f}" if (obj.stockinformationhistory.forwardPER is not None) else None,
            "forwardPSR" : f"{obj.stockinformationhistory.forwardPSR:.2f}" if (obj.stockinformationhistory.forwardPSR is not None) else None,
            "marketCap" : f"{obj.stockinformationhistory.marketCap:.2f}" if (obj.stockinformationhistory.marketCap is not None) else None,
            "ttmpEPS" : f"{obj.stockinformationhistory.ttmEPS:.2f}" if (obj.stockinformationhistory.ttmEPS is not None) else None
        })
        

class StockYearlyFinancialStatementsAPIView(RetrieveAPIView): 
    serializer_class = StockYearlyFinancialStatementsSerializer

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return_dict = dict()
        return_dict["dateArray"] = list()
        return_dict["revenueArray"] = list()
        return_dict["costOfRevenueArray"] = list()
        return_dict["grossProfit"] = list() 
        return_dict["operatingExpense"] = list()
        return_dict["operatingIncome"] = list()
        return_dict["basicEpsArray"] = list() # ttmEPS
        return_dict["dilutedEpsArray"] = list() # ttmEPS
        
        for idx, item in enumerate(serializer.data):
            iter_dict = json.loads(json.dumps(item))
            tmp_dict = json.loads(iter_dict["yearly_income_statement"])
            try: 
                tmp_dict = {key:tmp_dict[key] for key in sorted(tmp_dict)} 
                return_dict["dateArray"] = tmp_dict.keys() 
            except KeyError: 
                return_dict["dateArray"] = None 
            try: 
                return_dict["revenueArray"] = [tmp_dict[key]["totalRevenue"] for key in tmp_dict.keys()]
            except KeyError: 
                return_dict["revenueArray"] = None 
            try: 
                return_dict["costOfRevenueArray"] = [tmp_dict[key]["costOfRevenue"] for key in tmp_dict.keys()]        
            except KeyError: 
                return_dict["costOfRevenueArray"] = None 
            try: 
                return_dict["grossProfit"] = [tmp_dict[key]["grossProfit"] for key in tmp_dict.keys()]  
            except KeyError: 
                return_dict["grossProfit"] = None 
            try: 
                return_dict["operatingExpense"] = [tmp_dict[key]["totalOperatingExpenses"] for key in tmp_dict.keys()]
            except: 
                return_dict["operatingExpense"] = None 
            try: 
                return_dict["operatingIncome"] = [tmp_dict[key]["operatingIncome"] for key in tmp_dict.keys()]
            except KeyError: 
                return_dict["operatingIncome"] = None 
            return_dict["basicEpsArray"].append(iter_dict["ttmEPS"])
            return_dict["dilutedEpsArray"].append(iter_dict["ttmEPS"])

        return Response(return_dict)


class StockQuarterlyFinancialStatementsAPIView(RetrieveAPIView):
    serializer_class = StockQuarterlyFinancialStatementsSerializer

    def get_queryset(self):
        return StockInformationHistory.objects.filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return_dict = dict()
        return_dict["dateArray"] = list()
        return_dict["revenueArray"] = list()
        return_dict["costOfRevenueArray"] = list()
        return_dict["grossProfit"] = list() 
        return_dict["operatingExpense"] = list()
        return_dict["operatingIncome"] = list()
        return_dict["basicEpsArray"] = list() # ttmEPS
        return_dict["dilutedEpsArray"] = list() # ttmEPS

        for idx, item in enumerate(serializer.data):
            iter_dict = json.loads(json.dumps(item))
            tmp_dict = json.loads(iter_dict["quarterly_income_statement"])
            try: 
                tmp_dict = {key:tmp_dict[key] for key in sorted(tmp_dict)} 
                return_dict["dateArray"] = tmp_dict.keys() 
            except KeyError: 
                return_dict["dateArray"] = None
            try: 
                return_dict["revenueArray"] = [tmp_dict[key]["totalRevenue"] for key in tmp_dict.keys()]
            except KeyError: 
                return_dict["revenueArray"] = None 
            try: 
                return_dict["costOfRevenueArray"] = [tmp_dict[key]["costOfRevenue"] for key in tmp_dict.keys()]  
            except KeyError: 
                return_dict["costOfRevenueArray"] = None
            try: 
                return_dict["grossProfit"] = [tmp_dict[key]["grossProfit"] for key in tmp_dict.keys()]  
            except KeyError: 
                return_dict["grossProfit"] = None
            try: 
                return_dict["operatingExpense"] = [tmp_dict[key]["totalOperatingExpenses"] for key in tmp_dict.keys()]
            except: 
                return_dict["operatingExpense"] = None 
            try: 
                return_dict["operatingIncome"] = [tmp_dict[key]["operatingIncome"] for key in tmp_dict.keys()]
            except KeyError: 
                return_dict["operatingIncome"] = None 
            return_dict["basicEpsArray"].append(iter_dict["ttmEPS"])
            return_dict["dilutedEpsArray"].append(iter_dict["ttmEPS"])

        return Response(return_dict)


class StockProfileAPIView(RetrieveAPIView):
    serializer_class = StockProfileSerializer

    def get_queryset(self):
        return StockProfile.objects.filter(ticker=self.kwargs["ticker"])

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return_dict = dict()
        return_dict["name"] = list()
        return_dict["title"] = list()
        return_dict["pay"] = list()
        return_dict["age"] = list()
        return_dict["detailList"] = list()

        for idx, item in enumerate(serializer.data): 
            iter_dict = json.loads(json.dumps(item))
            tmp_dict = json.loads(iter_dict["company_officers"]) 
            ceo_idx = []
            
            for idx in range(len(tmp_dict)): 
                if re.search("CEO", tmp_dict[idx]["title"], re.I): ceo_idx.append(idx) 
            try: 
                return_dict["name"] = [tmp_dict[idx]["name"] for idx in ceo_idx]
            except KeyError: 
                return_dict["name"] = None
            for idx in ceo_idx: 
                try:
                    return_dict["title"].append(tmp_dict[idx]["title"])
                except KeyError: 
                    return_dict["title"].append(None)
            for idx in ceo_idx: 
                try:
                    return_dict["pay"].append(tmp_dict[idx]["totalPay"])
                except KeyError: 
                    return_dict["pay"].append(None)
            for idx in ceo_idx: 
                try:
                    return_dict["age"].append(tmp_dict[idx]["age"])
                except KeyError: 
                    return_dict["age"].append(None)
            for idx in ceo_idx: 
                try:
                    return_dict["detailList"].append(tmp_dict[idx]["detailList"])
                except KeyError: 
                    return_dict["detailList"].append(list())

        return Response(return_dict) 
