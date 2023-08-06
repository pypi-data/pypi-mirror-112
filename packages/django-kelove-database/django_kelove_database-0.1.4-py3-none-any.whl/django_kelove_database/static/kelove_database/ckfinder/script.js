window.addEventListener('error', function (e) {
    let target = e.target;
    let targetId = target.id;
    let tagName = target.tagName;
    let times = Number(target.dataset.times) || 0;
    let allTimes = 3;

    try {
        if (tagName.toUpperCase() === 'IMG' && times < allTimes) {
            document.getElementById(targetId).src = target.getAttribute("data-error-image");
        }
    } catch (e) {
        target.dataset.times = times + 1;
    }
}, true)

function selectFileWithCKFinderDjango(obj, key) {
    let elementId = getCkfinderControllerBtnElementId(obj, key);
    let imgInputId = elementId + '_ckfinder_img'
    selectFileWithCKFinder(elementId, imgInputId)
}

function delFileWithCKFinderDjango(obj, key) {
    let elementId = getCkfinderControllerBtnElementId(obj, key);
    let imgInputId = elementId + '_ckfinder_img'
    delFileWithCKFinder(elementId, imgInputId)
}

function getCkfinderControllerBtnElementId(obj, key) {
    let prefix = 'ckfinder-controller-btn-' + key;
    return obj.id.replace(prefix, '');
}

function selectFileWithCKFinder(elementId, img_id) {
    let config;
    try {
        let config_str = document.getElementById(elementId).attributes["field_settings"].nodeValue;
        config = JSON.parse(config_str);
    } catch (e) {
        config = {};
    }
    config = Object.assign({
        displayFoldersPanel: false,
        skin: 'neko',
        chooseFiles: true,
        width: 800,
        height: 600,
        plugins: ['ClearCache'],
    }, config);

    config.onInit = function (finder) {
        finder.on('files:choose', function (evt) {
            let file = evt.data.files.first();
            document.getElementById(elementId).value = file.getUrl();
            document.getElementById(img_id).src = file.getUrl();
        });

        finder.on('file:choose:resizedImage', function (evt) {
            document.getElementById(elementId).value = evt.data.resizedUrl;
            document.getElementById(img_id).src = evt.data.resizedUrl;
        });
    };
    localStorage.removeItem('ckf.settings');
    CKFinder.modal(config);
}

function delFileWithCKFinder(elementId, img_id) {
    document.getElementById(elementId).value = '';
    document.getElementById(img_id).src = '';
}