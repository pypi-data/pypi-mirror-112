/** Markdown 编辑器 整合 ckfinder文件选择 */
function editorMdSelectFileWithCKFinder(editormd_obj, ckfinder_editorConfig) {
    ckfinder_editorConfig = Object.assign({
        chooseFiles: true,
        width: 800,
        height: 600,
    }, ckfinder_editorConfig)
    ckfinder_editorConfig.onInit = function (finder) {
        finder.on('files:choose', function (evt) {
            let _img_url = evt.data.files.first().getUrl();
            let _content = '![' + _img_url + '](' + _img_url + ' "' + _img_url + '")';
            editormd_obj.insertValue(_content);
        });

        finder.on('file:choose:resizedImage', function (evt) {
            let _img_url = evt.data.resizedUrl;
            let _content = '![' + _img_url + '](' + _img_url + ' "' + _img_url + '")';
            editormd_obj.insertValue(_content);
        });
    };
    localStorage.removeItem('ckf.settings');
    CKFinder.modal(ckfinder_editorConfig);
}

/** 整合编辑器配置 */
function getEditorMdConfig(editorTextareaId, editorId) {
    let _editorId = editorId;

    let _editorConfig = {};
    try {
        _editorConfig = document.getElementById(editorTextareaId).attributes["field_settings"].nodeValue;
        _editorConfig = JSON.parse(_editorConfig);
    } catch (e) {
        _editorConfig = {};
    }

    if (_editorConfig.imageUpload === true && typeof _editorConfig.imageUploadURL === "object") {
        _editorConfig.toolbarIcons = function () {
            let _icons = editormd.toolbarModes['full'];
            if (_icons.indexOf('ckfinder') >= 0) {
                _icons.splice(_icons.indexOf('ckfinder'), 1);
            }

            if (_icons.indexOf('image') >= 0) {
                _icons.splice(_icons.indexOf('image'), 1);
            }
            _icons.splice(_icons.indexOf('reference-link') + 1, 0, "ckfinder");
            return _icons;
        };
        _editorConfig.toolbarIconsClass = {
            ckfinder: "fa-image"
        }
        _editorConfig.toolbarIconTexts = {
            ckfinder: "CKFinder"
        }
        _editorConfig.toolbarHandlers = {
            ckfinder: function (cm, icon, cursor, selection) {
                editorMdSelectFileWithCKFinder(this, _editorConfig.imageUploadURL);
            },
        };
    }

    _editorConfig.path = document.getElementById(_editorId).getAttribute('data-lib-path');

    return _editorConfig;

}

/* 初始化编辑器 */
function initEditorMdDjango(editor_md__hidden_image_id, widget_attrs_id) {
    let prefix = 'editor_md__hidden_image_';
    let __widget_attrs_id = editor_md__hidden_image_id.replace(prefix, '')
    if (__widget_attrs_id === widget_attrs_id && __widget_attrs_id.indexOf('__prefix__') !== -1) {
        return;
    }
    let __widget_attrs_id_content = 'editor_md_' + __widget_attrs_id + '_content'
    editormd(__widget_attrs_id_content, getEditorMdConfig(__widget_attrs_id, __widget_attrs_id_content));
}