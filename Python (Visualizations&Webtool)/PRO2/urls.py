"""PRO2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import plots.views as MyViews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MyViews.HomePage),
    url(r'^dashmain/$', MyViews.HomeDash),
    url(r'^dashmain/([^/]+)/$', MyViews.DiseaseDash),
    url(r'^dashmain/([^/]+)/([^/]+)/$', MyViews.TissueDashIntro),
    url(r'^diseaseselectorwizard/([^/]+)/([^/]+)/$', MyViews.TissueDash),
    url(r'^dashmain/([^/]+)/([^/]+)/([^/]+)~([^/]+)/$', MyViews.PlotTypeDash),
    url(r'^dashmain/([^/]+)/([^/]+)/([^/]+)/$', MyViews.PlotTypeDashIntro),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', MyViews.HomeDash), # Allauth social-login redirects to accounts/profile/ after login
    url(r'^UC/$', MyViews.UndiConsti),
    url(r'^tutorial/$', MyViews.TutorialShower),
    url(r'^about/$', MyViews.AboutShower),
    url(r'^privacy/$', MyViews.PrivacyShower),
    url(r'^terms/$', MyViews.TermsShower),
    url(r'^help/$', MyViews.HelpShower),

    url(r'^topo/([^/]+)/([^/]+)/$', MyViews.Actual3DPlotter),
    url(r'^2D/([^/]+)/([^/]+)/$', MyViews.Actual2DPlotter),
    url(r'^polar/([^/]+)/([^/]+)/$', MyViews.ActualPolarPlotter),
]
