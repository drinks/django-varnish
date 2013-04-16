from django.http import HttpResponseRedirect
from manager import manager
from django.views.generic import TemplateView
from django.conf import settings


class ManagementView(TemplateView):
    def get_stats(self):
        stats = [x[0] for x in manager.run('stats')]

        return zip(getattr(settings, 'VARNISH_MANAGEMENT_ADDRS', ()), stats)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        if 'command' in request.REQUEST:
            runkwargs = dict(request.REQUEST.items())
            manager.run(*str(runkwargs.pop('command')).split(), **kwargs)
            return HttpResponseRedirect(request.path)

        return super(ManagementView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ManagementView, self).get_context_data(**kwargs)
        try:
            stats = self.get_stats()
            errors = {}
        except:
            stats = None
            errors = {
                "stats": "Impossible to access the stats for server: %s" %
                getattr(settings, 'VARNISH_MANAGEMENT_ADDRS', ()),
            }
        ctx['stats'] = stats
        ctx['errors'] = errors

        return ctx
