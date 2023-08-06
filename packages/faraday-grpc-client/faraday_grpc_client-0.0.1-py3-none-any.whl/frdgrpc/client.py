from .common import BaseClient, faradayrpc
from .errors import handle_rpc_errors


class FaradayClient(BaseClient):
    @handle_rpc_errors
    def channel_insights(self):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.ChannelInsightsRequest()
        response = self._faraday_stub.ChannelInsights(request)
        return response

    @handle_rpc_errors
    def close_report(self, channel_point):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.CloseReportRequest(channel_point=channel_point)
        response = self._faraday_stub.CloseReport(request)
        return response

    @handle_rpc_errors
    def exchange_rate(self, **kwargs):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.ExchangeRateRequest(**kwargs)
        response = self._faraday_stub.ExchangeRate(request)
        return response

    @handle_rpc_errors
    def node_audit(self, **kwargs):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.NodeAuditRequest(**kwargs)
        response = self._faraday_stub.NodeAudit(request)
        return response

    @handle_rpc_errors
    def outlier_recommendations(self, **kwargs):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.OutlierRecommendationsRequest(**kwargs)
        response = self._faraday_stub.OutlierRecommendations(request)
        return response

    @handle_rpc_errors
    def revenue_report(self, **kwargs):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.RevenueReportRequest(**kwargs)
        response = self._faraday_stub.RevenueReport(request)
        return response

    @handle_rpc_errors
    def threshold_recommendations(self, **kwargs):
        """Unlock encrypted wallet at lnd startup"""
        request = faradayrpc.ThresholdRecommendationsRequest(**kwargs)
        response = self._faraday_stub.ThresholdRecommendations(request)
        return response