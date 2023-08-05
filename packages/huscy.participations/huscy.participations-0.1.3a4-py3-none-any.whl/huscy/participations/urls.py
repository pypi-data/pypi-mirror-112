from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import GenericViewSet
from rest_framework_nested.routers import NestedDefaultRouter

from huscy.participations import views


router = DefaultRouter()
router.register('experiments', GenericViewSet, basename='experiment')

experiment_router = NestedDefaultRouter(router, 'experiments', lookup='experiment')
experiment_router.register('subjectgroups', GenericViewSet, basename='subjectgroup')
experiment_router.register('participations', views.ListParticipationsViewSet,
                           basename='experiment-participation')

subjectgroup_router = NestedDefaultRouter(experiment_router, 'subjectgroups', lookup='subjectgroup')
subjectgroup_router.register('participations', views.ParticipationViewSet,
                             basename='subjectgroup-participation')


urlpatterns = router.urls
urlpatterns += experiment_router.urls
urlpatterns += subjectgroup_router.urls
