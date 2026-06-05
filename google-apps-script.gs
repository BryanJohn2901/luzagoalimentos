/**
 * Google Apps Script — Planilha automática de leads Luzago
 *
 * COMO CONFIGURAR:
 * 1. Crie uma planilha no Google Sheets com 3 abas:
 *    - Leads Comerciais
 *    - Curriculos
 *    - Fornecedores
 * 2. Em cada aba, crie a linha 1 com os cabeçalhos:
 *    Data | Nome/Empresa | Email | Telefone | Categoria | Mensagem/Produtos | Origem | Campanha | Página | Referrer | GCLID
 * 3. Extensões → Apps Script → cole este código
 * 4. Altere SPREADSHEET_ID para o ID da sua planilha
 * 5. Implantar → Nova implantação → App da Web
 *    - Executar como: Eu
 *    - Quem tem acesso: Qualquer pessoa
 * 6. Copie a URL gerada e cole em js/leads.js (SHEETS_WEB_APP_URL)
 */

var SPREADSHEET_ID = 'COLE_O_ID_DA_PLANILHA_AQUI';

var SHEETS = {
  comercial: 'Leads Comerciais',
  curriculo: 'Curriculos',
  fornecedor: 'Fornecedores'
};

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheetName = SHEETS[data.lead_type] || 'Leads Comerciais';
    var sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(sheetName);
    var fields = data.fields || {};
    var source = data.source || {};

    var row = [
      data.submitted_at || new Date(),
      fields.empresa || fields.nome || '',
      fields.email || '',
      fields.telefone || '',
      fields.categoria || '',
      fields.produtos || fields.mensagem || '',
      source.utm_source || '',
      source.utm_campaign || '',
      source.page || '',
      source.referrer || '',
      source.gclid || ''
    ];

    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService
    .createTextOutput('Luzago Leads API ativa')
    .setMimeType(ContentService.MimeType.TEXT);
}
