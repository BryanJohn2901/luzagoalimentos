/**
 * Luzago Alimentos — captura de leads
 *
 * Configure SHEETS_WEB_APP_URL após publicar o Google Apps Script
 * (arquivo google-apps-script.gs na raiz do projeto).
 *
 * Tipos de formulário (data-lead-form):
 *   comercial  → leads comerciais (não contabilizar como fornecedor/currículo)
 *   curriculo  → envio de currículo
 *   fornecedor → cadastro de fornecedor
 */
(function () {
    'use strict';

    var SHEETS_WEB_APP_URL = (window.LUZAGO_RUNTIME && window.LUZAGO_RUNTIME.sheetsWebAppUrl) || '';

    function captureLeadSource() {
        var params = new URLSearchParams(window.location.search);
        var source = {
            utm_source: params.get('utm_source') || '',
            utm_medium: params.get('utm_medium') || '',
            utm_campaign: params.get('utm_campaign') || '',
            utm_term: params.get('utm_term') || '',
            utm_content: params.get('utm_content') || '',
            gclid: params.get('gclid') || '',
            page: window.location.pathname,
            referrer: document.referrer || '',
            captured_at: new Date().toISOString()
        };

        var hasTracking = source.utm_source || source.utm_campaign || source.gclid;
        if (hasTracking || !sessionStorage.getItem('luzago_lead_source')) {
            sessionStorage.setItem('luzago_lead_source', JSON.stringify(source));
        }

        try {
            return JSON.parse(sessionStorage.getItem('luzago_lead_source') || '{}');
        } catch (e) {
            return source;
        }
    }

    function formToObject(form) {
        var data = {};
        var formData = new FormData(form);
        formData.forEach(function (value, key) {
            if (data[key]) {
                if (!Array.isArray(data[key])) data[key] = [data[key]];
                data[key].push(value);
            } else {
                data[key] = value;
            }
        });
        return data;
    }

    function showMessage(form, type, text) {
        var box = form.querySelector('[data-form-message]');
        if (!box) {
            box = document.createElement('div');
            box.setAttribute('data-form-message', '');
            box.className = 'rounded px-4 py-3 text-sm mt-4';
            form.appendChild(box);
        }
        box.className = 'rounded px-4 py-3 text-sm mt-4 ' +
            (type === 'success' ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-800 border border-red-200');
        box.textContent = text;
        box.hidden = false;
    }

    function setLoading(form, loading) {
        var btn = form.querySelector('[type="submit"]');
        if (!btn) return;
        if (loading) {
            btn.dataset.originalText = btn.textContent;
            btn.disabled = true;
            btn.textContent = 'Enviando...';
        } else {
            btn.disabled = false;
            btn.textContent = btn.dataset.originalText || 'Enviar';
        }
    }

    async function submitLead(form) {
        var leadType = form.getAttribute('data-lead-form');
        var source = captureLeadSource();
        var payload = {
            lead_type: leadType,
            source: source,
            fields: formToObject(form),
            submitted_at: new Date().toISOString()
        };

        if (!SHEETS_WEB_APP_URL) {
            console.info('[Luzago Leads] Payload pronto para envio:', payload);
            showMessage(form, 'success', 'Recebemos seu contato! Em breve nossa equipe retornará.');
            form.reset();
            return;
        }

        var response = await fetch(SHEETS_WEB_APP_URL, {
            method: 'POST',
            mode: 'no-cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        showMessage(form, 'success', 'Recebemos seu contato! Em breve nossa equipe retornará.');
        form.reset();
    }

    function initFileLabels() {
        document.querySelectorAll('input[type="file"][data-file-label]').forEach(function (input) {
            var labelId = input.getAttribute('data-file-label');
            var label = document.getElementById(labelId);
            if (!label) return;
            input.addEventListener('change', function () {
                if (input.files && input.files[0]) {
                    label.innerHTML = '<i class="fa-solid fa-file-lines"></i><span>' + input.files[0].name + '</span>';
                }
            });
        });
    }

    function initForms() {
        captureLeadSource();

        document.querySelectorAll('form[data-lead-form]').forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                setLoading(form, true);
                submitLead(form)
                    .catch(function () {
                        showMessage(form, 'error', 'Não foi possível enviar agora. Tente novamente ou ligue (41) 3668-7866.');
                    })
                    .finally(function () {
                        setLoading(form, false);
                    });
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initForms();
        initFileLabels();
    });
})();
