(self["webpackChunkjupyterlab_notify"] = self["webpackChunkjupyterlab_notify"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/desktop-notify+json';
const PROCESSED_KEY = 'isProcessed';
// The below can be used to customize notifications
const NOTIFICATION_OPTIONS = {
    icon: '/static/favicons/favicon.ico'
};
/**
 * A widget for rendering desktop-notify.
 */
class OutputWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(options) {
        super();
        this._mimeType = options.mimeType;
    }
    renderModel(model) {
        const mimeData = model.data[this._mimeType];
        const payload = mimeData.payload;
        // If the PROCESSED_KEY is available - do not take any action
        // This is done so that notifications are not repeated on page refresh
        if (mimeData[PROCESSED_KEY]) {
            return Promise.resolve();
        }
        // For first-time users, check for necessary permissions and prompt if needed
        if ((mimeData.type === 'INIT' && Notification.permission === 'default') ||
            Notification.permission !== 'granted') {
            // We do not have any actions to perform upon acquiring permission and so
            // handle only the errors (if any)
            Notification.requestPermission().catch(err => {
                alert(`Encountered error - ${err} while requesting permissions for notebook notifications`);
            });
        }
        if (mimeData.type === 'NOTIFY') {
            // Notify only if there's sufficient permissions and this has not been processed previously
            if (Notification.permission === 'granted' && !mimeData[PROCESSED_KEY]) {
                new Notification(payload.title, NOTIFICATION_OPTIONS);
            }
            else {
                this.node.innerHTML = `<div id="${mimeData.id}">Missing permissions - update "Notifications" preferences under browser settings to receive notifications</div>`;
            }
        }
        if (!mimeData[PROCESSED_KEY]) {
            // Add isProcessed property to each notification message so that we can avoid repeating notifications on page reloads
            const updatedModel = JSON.parse(JSON.stringify(model));
            const updatedMimeData = updatedModel.data[this._mimeType];
            updatedMimeData[PROCESSED_KEY] = true;
            // The below model update is done inside a separate function and added to
            // the event queue - this is done so to avoid re-rendering before the
            // initial render is complete.
            //
            // Without the setTimeout, calling model.setData triggers the callbacks
            // registered on model-updates that re-renders the widget and it again tries
            // to update the model which again causes a re-render and so on.
            setTimeout(() => {
                model.setData(updatedModel);
            }, 0);
        }
        return Promise.resolve();
    }
}
/**
 * A mime renderer factory for desktop-notify data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE],
    createRenderer: options => new OutputWidget(options)
};
/**
 * Extension definition.
 */
const extension = {
    id: 'desktop-notify:plugin',
    rendererFactory,
    rank: 0,
    dataType: 'json'
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.d51437c461ac03fb8217.js.map