from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView as BaseView


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class CustomGraphQLViewMixin(BaseView):

    @classonlymethod
    def as_view(cls, **initkwargs):
        fn = super().as_view(**initkwargs)
        return csrf_exempt(fn)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            reason = self.enforce_csrf(request)
            if reason:
                return JsonResponse(data={'error': 'CSRF Failed: %s' % reason})
        return super().dispatch(request, *args, **kwargs)

    #From django_rest_framework SessionAuthentication
    def enforce_csrf(self, request):
        def dummy_get_response(request):
            return None
        check = CSRFCheck(dummy_get_response)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        return reason
