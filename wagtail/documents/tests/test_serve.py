import unittest
from unittest.mock import patch, MagicMock
from django.http import Http404
from django.shortcuts import redirect
from django.test import RequestFactory
from documents.views import serve


class TestServe(unittest.TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.mock_document = MagicMock()
        self.mock_document.file.url = "http://example.com/document"
        self.mock_document.file.path = "/path/to/document"
        self.mock_document.filename = "document.pdf"
        self.mock_document.content_type = "application/pdf"
        self.mock_document.content_disposition = "inline"
    
    # CT1
    @patch("path.to.module.get_document_model")
    @patch("path.to.module.get_object_or_404")
    @patch("path.to.module.settings")
    def test_CT1_nao_precisa_redirecionar(self, mock_settings, mock_get_object_or_404, mock_get_document_model):
       
        mock_settings.WAGTAILDOCS_SERVE_METHOD = None
        self.mock_document.file.url = True
        self.mock_document.file.path = True
        mock_get_document_model.return_value = MagicMock()
        mock_get_object_or_404.return_value = self.mock_document

        response = serve(self.request, document_id=1, document_filename="document.pdf")

        # Saída Esperada: serve_view (não redireciona)
        self.assertNotEqual(response.status_code, 302)

    # CT2
    @patch("path.to.module.get_document_model")
    @patch("path.to.module.get_object_or_404")
    @patch("path.to.module.settings")
    def test_CT2_caminho_local_inexistente(self, mock_settings, mock_get_object_or_404, mock_get_document_model):
        
        mock_settings.WAGTAILDOCS_SERVE_METHOD = "redirect"
        self.mock_document.file.url = True
        self.mock_document.file.path = False
        mock_get_document_model.return_value = MagicMock()
        mock_get_object_or_404.return_value = self.mock_document

        response = serve(self.request, document_id=1, document_filename="document.pdf")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "http://example.com/document")

    # CT3
    @patch("path.to.module.get_document_model")
    @patch("path.to.module.get_object_or_404")
    @patch("path.to.module.settings")
    def test_CT3_url_direta_inexistente(self, mock_settings, mock_get_object_or_404, mock_get_document_model):
    
        mock_settings.WAGTAILDOCS_SERVE_METHOD = None
        self.mock_document.file.url = False
        self.mock_document.file.path = True
        mock_get_document_model.return_value = MagicMock()
        mock_get_object_or_404.return_value = self.mock_document

        with self.assertRaises(Http404):
            serve(self.request, document_id=1, document_filename="document.pdf")

    # CT4
    @patch("path.to.module.get_document_model")
    @patch("path.to.module.get_object_or_404")
    @patch("path.to.module.settings")
    def test_CT4_redireciona_url_direta(self, mock_settings, mock_get_object_or_404, mock_get_document_model):
        
        mock_settings.WAGTAILDOCS_SERVE_METHOD = "direct"
        self.mock_document.file.url = True
        mock_get_document_model.return_value = MagicMock()
        mock_get_object_or_404.return_value = self.mock_document

        response = serve(self.request, document_id=1, document_filename="document.pdf")

        # Saída Esperada: Redireciona
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "http://example.com/document")

    # CT5
    @patch("path.to.module.get_document_model")
    @patch("path.to.module.get_object_or_404")
    @patch("path.to.module.settings")
    def test_CT5_url_direta_nao_disponivel(self, mock_settings, mock_get_object_or_404, mock_get_document_model):

        mock_settings.WAGTAILDOCS_SERVE_METHOD = "redirect"
        self.mock_document.file.url = False
        mock_get_document_model.return_value = MagicMock()
        mock_get_object_or_404.return_value = self.mock_document

        with self.assertRaises(Http404):
            serve(self.request, document_id=1, document_filename="document.pdf")

    # CT6
    @patch("path.to.module.get_document_model")
    @patch("path.to.module.get_object_or_404")
    @patch("path.to.module.settings")
    def test_CT6_metodo_entrega_invalido(self, mock_settings, mock_get_object_or_404, mock_get_document_model):
        
        mock_settings.WAGTAILDOCS_SERVE_METHOD = "invalido"
        self.mock_document.file.url = True
        mock_get_document_model.return_value = MagicMock()
        mock_get_object_or_404.return_value = self.mock_document

        with self.assertRaises(Http404):
            serve(self.request, document_id=1, document_filename="document.pdf")


