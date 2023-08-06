function keloveJsonEditorInit(json_editor_hidden_image_id, widget_attrs_id) {
    let prefix = 'json_editor_hidden_image_';
    let json_editor_controller_id = json_editor_hidden_image_id.replace(prefix, '');
    if (json_editor_controller_id === widget_attrs_id && json_editor_controller_id.indexOf('__prefix__') !== -1) {
        return;
    }
    let _editor_id = 'json_editor_' + json_editor_controller_id;
    let jsonValue = document.getElementById(json_editor_controller_id).value;
    try {
        jsonValue = JSON.parse(jsonValue);
    } catch (e) {
        jsonValue = jsonValue.replace(/[\r\n]/g, '');
    }
    let _editorConfig;
    try {
        _editorConfig = document.getElementById(json_editor_controller_id).attributes["field_settings"].nodeValue;
        _editorConfig = JSON.parse(_editorConfig);
    } catch (e) {
        _editorConfig = {};
    }

    _editorConfig.onChangeText = function (jsonString) {
        document.getElementById(json_editor_controller_id).value = jsonString;
    };
    (new JSONEditor(document.getElementById(_editor_id), _editorConfig)).set(jsonValue);
}