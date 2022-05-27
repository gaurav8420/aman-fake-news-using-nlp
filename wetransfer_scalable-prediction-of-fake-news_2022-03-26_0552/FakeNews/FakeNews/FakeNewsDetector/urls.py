from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("Login.html", views.Login, name="Login"),
	       path("AdminLogin", views.AdminLogin, name="AdminLogin"),
	       path("UploadNews.html", views.UploadNews, name="UploadNews"),
	       path("UploadNewsDocument", views.UploadNewsDocument, name="UploadNewsDocument"),
	       path("DetectorAlgorithm", views.DetectorAlgorithm, name="DetectorAlgorithm"),
]