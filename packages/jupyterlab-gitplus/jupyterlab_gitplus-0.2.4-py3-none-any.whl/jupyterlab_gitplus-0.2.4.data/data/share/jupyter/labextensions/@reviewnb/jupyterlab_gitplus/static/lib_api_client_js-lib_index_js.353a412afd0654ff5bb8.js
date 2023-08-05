(self["webpackChunk_reviewnb_jupyterlab_gitplus"] = self["webpackChunk_reviewnb_jupyterlab_gitplus"] || []).push([["lib_api_client_js-lib_index_js"],{

/***/ "./lib/api_client.js":
/*!***************************!*\
  !*** ./lib/api_client.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HTTP": () => (/* binding */ HTTP),
/* harmony export */   "get_server_config": () => (/* binding */ get_server_config),
/* harmony export */   "get_modified_repositories": () => (/* binding */ get_modified_repositories),
/* harmony export */   "create_pull_request": () => (/* binding */ create_pull_request),
/* harmony export */   "create_and_push_commit": () => (/* binding */ create_and_push_commit)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! axios */ "webpack/sharing/consume/default/axios/axios");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./index */ "./lib/index.js");




const HTTP = axios__WEBPACK_IMPORTED_MODULE_2___default().create({
    baseURL: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getBaseUrl()
});
HTTP.defaults.headers.post['X-CSRFToken'] = _get_cookie('_xsrf');
function _get_cookie(name) {
    // Source: https://blog.jupyter.org/security-release-jupyter-notebook-4-3-1-808e1f3bb5e2
    const r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return r ? r[1] : undefined;
}
function get_server_config() {
    return HTTP.get('gitplus/expanded_server_root')
        .then(response => {
        return response.data;
    })
        .catch(error => {
        console.log(error);
    });
}
function get_modified_repositories(data, show_repository_selection_dialog, command, show_repository_selection_failure_dialog) {
    const repo_names = [];
    return HTTP.post('gitplus/modified_repo', data)
        .then(response => {
        const repo_list = response.data;
        for (const repo of repo_list) {
            const display_name = repo['name'] + ' (' + repo['path'] + ')';
            repo_names.push([display_name, repo['path']]);
        }
        show_repository_selection_dialog(repo_names, command);
    })
        .catch(error => {
        show_repository_selection_failure_dialog();
        console.log(error);
    });
}
function create_pull_request(data, show_pr_created_dialog) {
    (0,_index__WEBPACK_IMPORTED_MODULE_3__.show_spinner)();
    return HTTP.post('gitplus/pull_request', data)
        .then(response => {
        const result = response.data;
        const github_url = result['github_url'];
        const reviewnb_url = result['reviewnb_url'];
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.flush(); // remove spinner
        show_pr_created_dialog(github_url, reviewnb_url);
    })
        .catch(error => {
        console.log(error);
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.flush(); // remove spinner
        show_pr_created_dialog();
    });
}
function create_and_push_commit(data, show_commit_pushed_dialog) {
    (0,_index__WEBPACK_IMPORTED_MODULE_3__.show_spinner)();
    return HTTP.post('gitplus/commit', data)
        .then(response => {
        const result = response.data;
        const github_url = result['github_url'];
        const reviewnb_url = result['reviewnb_url'];
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.flush(); // remove spinner
        show_commit_pushed_dialog(github_url, reviewnb_url);
    })
        .catch(error => {
        console.log(error);
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.flush(); // remove spinner
        show_commit_pushed_dialog();
    });
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "show_repository_selection_failure_dialog": () => (/* binding */ show_repository_selection_failure_dialog),
/* harmony export */   "show_file_selection_failure_dialog": () => (/* binding */ show_file_selection_failure_dialog),
/* harmony export */   "show_spinner": () => (/* binding */ show_spinner),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _utility__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./utility */ "./lib/utility.js");
/* harmony import */ var _api_client__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./api_client */ "./lib/api_client.js");
/* harmony import */ var _ui_elements__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./ui_elements */ "./lib/ui_elements.js");








/**
 * The plugin registration information.
 */
const gitPlusPlugin = {
    activate,
    requires: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorTracker, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker],
    id: '@reviewnb/gitplus',
    autoStart: true
};
/**
 * Activate the extension.
 */
function activate(app, mainMenu, editorTracker, notebookTracker) {
    console.log('JupyterLab extension @reviewnb/gitplus (0.1.5) is activated!');
    const createPRCommand = 'create-pr';
    app.commands.addCommand(createPRCommand, {
        label: 'Create Pull Request',
        execute: () => {
            (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.get_server_config)()
                .then(config => {
                const files = get_open_files(editorTracker, notebookTracker, config['server_root_dir']);
                const data = (0,_utility__WEBPACK_IMPORTED_MODULE_6__.get_json_request_payload_from_file_list)(files);
                (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.get_modified_repositories)(data, show_repository_selection_dialog, createPRCommand, show_repository_selection_failure_dialog);
            })
                .catch(error => {
                show_repository_selection_failure_dialog();
                console.log(error);
            });
        }
    });
    const pushCommitCommand = 'push-commit';
    app.commands.addCommand(pushCommitCommand, {
        label: 'Push Commit',
        execute: () => {
            (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.get_server_config)()
                .then(config => {
                const files = get_open_files(editorTracker, notebookTracker, config['server_root_dir']);
                const data = (0,_utility__WEBPACK_IMPORTED_MODULE_6__.get_json_request_payload_from_file_list)(files);
                (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.get_modified_repositories)(data, show_repository_selection_dialog, pushCommitCommand, show_repository_selection_failure_dialog);
            })
                .catch(error => {
                show_repository_selection_failure_dialog();
                console.log(error);
            });
        }
    });
    function show_repository_selection_dialog(repo_names, command) {
        if (repo_names.length == 0) {
            let msg = "No GitHub repositories found! \n\nFirst, open the files that you'd like to commit or create pull request for.";
            if (command == createPRCommand) {
                msg =
                    "No GitHub repositories found! \n\nFirst, open the files that you'd like to create pull request for.";
            }
            else if (command == pushCommitCommand) {
                msg =
                    "No GitHub repositories found! \n\nFirst, open the files that you'd like to commit.";
            }
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Repository Selection',
                body: msg,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Okay' })]
            }).then(result => { });
        }
        else {
            const label_style = {
                'font-size': '14px'
            };
            const body_style = {
                'padding-top': '2em',
                'padding-bottom': '2em',
                'border-top': '1px solid #dfe2e5'
            };
            const select_style = {
                'margin-top': '4px',
                'min-height': '32px'
            };
            const styles = {
                label_style: label_style,
                body_style: body_style,
                select_style: select_style
            };
            const dwidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.DropDown(repo_names, 'Select Repository', styles);
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Repository Selection',
                body: dwidget,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Next' })]
            }).then(result => {
                if (!result.button.accept) {
                    return;
                }
                const repo_name = dwidget.getTo();
                show_file_selection_dialog(repo_name, command);
            });
        }
    }
    function show_file_selection_dialog(repo_path, command) {
        (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.get_server_config)()
            .then(config => {
            const files = get_open_files(editorTracker, notebookTracker, config['server_root_dir']);
            const relevant_files = [];
            for (const f of files) {
                if (f.startsWith(repo_path)) {
                    relevant_files.push(f.substring(repo_path.length + 1));
                }
            }
            const cwidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.CheckBoxes(relevant_files);
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Select Files',
                body: cwidget,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Next' })]
            }).then(result => {
                if (!result.button.accept) {
                    return;
                }
                const files = cwidget.getSelected();
                if (command == createPRCommand) {
                    show_commit_pr_message_dialog(repo_path, files);
                }
                else if (command == pushCommitCommand) {
                    show_commit_message_dialog(repo_path, files);
                }
            });
        })
            .catch(error => {
            show_file_selection_failure_dialog();
            console.log(error);
        });
    }
    function show_commit_message_dialog(repo_path, files) {
        console.log(`${repo_path} --show_commit_message_dialog-- ${files}`);
        const cmwidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.CommitMessageDialog();
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: 'Provide Details',
            body: cmwidget,
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Create & Push Commit' })
            ]
        }).then(result => {
            if (!result.button.accept) {
                return;
            }
            const commit_message = cmwidget.getCommitMessage();
            const body = {
                files: files,
                repo_path: repo_path,
                commit_message: commit_message
            };
            (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.create_and_push_commit)(body, show_commit_pushed_dialog);
        });
    }
    function show_commit_pr_message_dialog(repo_path, files) {
        console.log(`${repo_path} --show_commit_pr_message_dialog-- ${files}`);
        const cprwidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.CommitPRMessageDialog();
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
            title: 'Provide Details',
            body: cprwidget,
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Create PR' })]
        }).then(result => {
            if (!result.button.accept) {
                return;
            }
            const commit_message = cprwidget.getCommitMessage();
            const pr_title = cprwidget.getPRTitle();
            const body = {
                files: files,
                repo_path: repo_path,
                commit_message: commit_message,
                pr_title: pr_title
            };
            (0,_api_client__WEBPACK_IMPORTED_MODULE_5__.create_pull_request)(body, show_pr_created_dialog);
        });
    }
    function show_pr_created_dialog(github_url = '', reviewnb_url = '') {
        if (github_url.length == 0 || reviewnb_url.length == 0) {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Failure',
                body: "Failed to create pull request. Check Jupyter logs for error. \n\nMake sure you've correctly setup GitHub access token. Steps here - https://github.com/ReviewNB/jupyterlab-gitplus/blob/master/README.md#setup-github-token\n\nIf unable to resolve, open an issue here - https://github.com/ReviewNB/jupyterlab-gitplus/issues",
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Okay' })]
            }).then(result => { });
        }
        else {
            const prcwidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.PRCreated(github_url, reviewnb_url);
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Pull Request Created',
                body: prcwidget,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Okay' })]
            }).then(result => { });
        }
    }
    function show_commit_pushed_dialog(github_url = '', reviewnb_url = '') {
        if (github_url.length == 0 || reviewnb_url.length == 0) {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Failure',
                body: 'Failed to create/push commit. Check Jupyter logs for error. \n\nIf unable to resolve, open an issue here - https://github.com/ReviewNB/jupyterlab-gitplus/issues',
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Okay' })]
            }).then(result => { });
        }
        else {
            const prcwidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.CommitPushed(github_url, reviewnb_url);
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Commit pushed!',
                body: prcwidget,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Okay' })]
            }).then(result => {
                if (!result.button.accept) {
                    return;
                }
            });
        }
    }
    // Create new top level menu
    const menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Menu({ commands: app.commands });
    menu.title.label = 'Git-Plus';
    mainMenu.addMenu(menu, { rank: 40 });
    // Add commands to menu
    menu.addItem({
        command: createPRCommand,
        args: {}
    });
    menu.addItem({
        command: pushCommitCommand,
        args: {}
    });
}
function show_repository_selection_failure_dialog() {
    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Failure', 'Failed to fetch list of repositories. Have you installed & enabled server side of the extension? \n\nSee installation steps here - https://github.com/ReviewNB/jupyterlab-gitplus/blob/master/README.md#install\n\nIf unable to resolve, open an issue here - https://github.com/ReviewNB/jupyterlab-gitplus/issues');
}
function show_file_selection_failure_dialog() {
    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Failure', 'Failed to fetch list of modified files. Have you installed & enabled server side of the extension? \n\nSee installation steps here - https://github.com/ReviewNB/jupyterlab-gitplus/blob/master/README.md#install\n\nIf unable to resolve, open an issue here - https://github.com/ReviewNB/jupyterlab-gitplus/issues');
}
function show_spinner() {
    const spinWidget = new _ui_elements__WEBPACK_IMPORTED_MODULE_7__.SpinnerDialog();
    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        title: 'Waiting for response...',
        body: spinWidget,
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton()]
    }).then(result => { });
}
function get_open_files(editorTracker, notebookTracker, base_dir) {
    const result = [];
    let separator = '/';
    if (base_dir.includes('\\')) {
        separator = '\\';
    }
    notebookTracker.forEach(notebook => {
        result.push(base_dir + separator + notebook.context.path);
    });
    editorTracker.forEach(editor => {
        result.push(base_dir + separator + editor.context.path);
    });
    return result;
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (gitPlusPlugin);


/***/ }),

/***/ "./lib/ui_elements.js":
/*!****************************!*\
  !*** ./lib/ui_elements.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SpinnerDialog": () => (/* binding */ SpinnerDialog),
/* harmony export */   "PRCreated": () => (/* binding */ PRCreated),
/* harmony export */   "CommitPushed": () => (/* binding */ CommitPushed),
/* harmony export */   "DropDown": () => (/* binding */ DropDown),
/* harmony export */   "CheckBoxes": () => (/* binding */ CheckBoxes),
/* harmony export */   "CommitPRMessageDialog": () => (/* binding */ CommitPRMessageDialog),
/* harmony export */   "CommitMessageDialog": () => (/* binding */ CommitMessageDialog)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);


class SpinnerDialog extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        const spinner_style = {
            'margin-top': '6em'
        };
        const body = document.createElement('div');
        const basic = document.createElement('div');
        Private.apply_style(basic, spinner_style);
        body.appendChild(basic);
        const spinner = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Spinner();
        basic.appendChild(spinner.node);
        super({ node: body });
    }
}
class PRCreated extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(github_url, reviewnb_url) {
        const anchor_style = {
            color: '#106ba3',
            'text-decoration': 'underline'
        };
        const body = document.createElement('div');
        const basic = document.createElement('div');
        basic.classList.add('gitPlusDialogBody');
        body.appendChild(basic);
        basic.appendChild(Private.buildLabel('See pull request on GitHub: '));
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildAnchor(github_url, github_url, anchor_style));
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildLabel('See pull request on ReviewNB: '));
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildAnchor(reviewnb_url, reviewnb_url, anchor_style));
        basic.appendChild(Private.buildNewline());
        super({ node: body });
    }
}
class CommitPushed extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(github_url, reviewnb_url) {
        const anchor_style = {
            color: '#106ba3',
            'text-decoration': 'underline'
        };
        const body = document.createElement('div');
        const basic = document.createElement('div');
        basic.classList.add('gitPlusDialogBody');
        body.appendChild(basic);
        basic.appendChild(Private.buildLabel('See commit on GitHub: '));
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildAnchor(github_url, github_url, anchor_style));
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildLabel('See commit on ReviewNB: '));
        basic.appendChild(Private.buildNewline());
        basic.appendChild(Private.buildAnchor(reviewnb_url, reviewnb_url, anchor_style));
        basic.appendChild(Private.buildNewline());
        super({ node: body });
    }
}
class DropDown extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(options = [], label = '', styles = {}) {
        let body_style = {};
        let label_style = {};
        let select_style = {};
        if ('body_style' in styles) {
            body_style = styles['body_style'];
        }
        if ('label_style' in styles) {
            label_style = styles['label_style'];
        }
        if ('select_style' in styles) {
            select_style = styles['select_style'];
        }
        const body = document.createElement('div');
        Private.apply_style(body, body_style);
        const basic = document.createElement('div');
        body.appendChild(basic);
        basic.appendChild(Private.buildLabel(label, label_style));
        basic.appendChild(Private.buildSelect(options, select_style));
        super({ node: body });
    }
    get toNode() {
        return this.node.getElementsByTagName('select')[0];
    }
    getTo() {
        return this.toNode.value;
    }
}
class CheckBoxes extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(items = []) {
        const basic = document.createElement('div');
        basic.classList.add('gitPlusDialogBody');
        for (const item of items) {
            basic.appendChild(Private.buildCheckbox(item));
        }
        super({ node: basic });
    }
    getSelected() {
        const result = [];
        const inputs = this.node.getElementsByTagName('input');
        for (const input of inputs) {
            if (input.checked) {
                result.push(input.id);
            }
        }
        return result;
    }
}
class CommitPRMessageDialog extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        const body = document.createElement('div');
        const basic = document.createElement('div');
        basic.classList.add('gitPlusDialogBody');
        body.appendChild(basic);
        basic.appendChild(Private.buildLabel('Commit message: '));
        basic.appendChild(Private.buildTextarea('Enter your commit message', 'gitplus-commit-message', 'gitPlusMessageTextArea'));
        basic.appendChild(Private.buildLabel('PR title: '));
        basic.appendChild(Private.buildTextarea('Enter title for pull request', 'gitplus-pr-message', 'gitPlusMessageTextArea'));
        super({ node: body });
    }
    getCommitMessage() {
        const textareas = this.node.getElementsByTagName('textarea');
        for (const textarea of textareas) {
            if (textarea.id == 'gitplus-commit-message') {
                return textarea.value;
            }
        }
        return '';
    }
    getPRTitle() {
        const textareas = this.node.getElementsByTagName('textarea');
        for (const textarea of textareas) {
            if (textarea.id == 'gitplus-pr-message') {
                return textarea.value;
            }
        }
        return '';
    }
}
class CommitMessageDialog extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        const body = document.createElement('div');
        const basic = document.createElement('div');
        basic.classList.add('gitPlusDialogBody');
        body.appendChild(basic);
        basic.appendChild(Private.buildLabel('Commit message: '));
        basic.appendChild(Private.buildTextarea('Enter your commit message', 'gitplus-commit-message', 'gitPlusMessageTextArea'));
        super({ node: body });
    }
    getCommitMessage() {
        const textareas = this.node.getElementsByTagName('textarea');
        for (const textarea of textareas) {
            if (textarea.id == 'gitplus-commit-message') {
                return textarea.value;
            }
        }
        return '';
    }
}
var Private;
(function (Private) {
    const default_none = document.createElement('option');
    default_none.selected = false;
    default_none.disabled = true;
    default_none.hidden = false;
    default_none.style.display = 'none';
    default_none.value = '';
    function buildLabel(text, style = {}) {
        const label = document.createElement('label');
        label.textContent = text;
        apply_style(label, style);
        return label;
    }
    Private.buildLabel = buildLabel;
    function buildAnchor(url, text, style = {}) {
        const anchor = document.createElement('a');
        anchor.href = url;
        anchor.text = text;
        anchor.target = '_blank';
        apply_style(anchor, style);
        return anchor;
    }
    Private.buildAnchor = buildAnchor;
    function buildNewline() {
        return document.createElement('br');
    }
    Private.buildNewline = buildNewline;
    function buildCheckbox(text) {
        const span = document.createElement('span');
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.classList.add('gitPlusCheckbox');
        input.id = text;
        input.type = 'checkbox';
        label.htmlFor = text;
        label.textContent = text;
        span.appendChild(input);
        span.appendChild(label);
        return span;
    }
    Private.buildCheckbox = buildCheckbox;
    function buildTextarea(text, id, _class) {
        const area = document.createElement('textarea');
        area.placeholder = text;
        area.id = id;
        area.classList.add(_class);
        return area;
    }
    Private.buildTextarea = buildTextarea;
    function buildSelect(list, style = {}, def) {
        const select = document.createElement('select');
        select.appendChild(default_none);
        for (const x of list) {
            const option = document.createElement('option');
            option.value = x[1];
            option.textContent = x[0];
            select.appendChild(option);
            if (def && x[0] === def) {
                option.selected = true;
            }
        }
        apply_style(select, style);
        return select;
    }
    Private.buildSelect = buildSelect;
    function apply_style(element, style) {
        if ('margin-top' in style) {
            element.style.marginTop = style['margin-top'];
        }
        if ('margin-bottom' in style) {
            element.style.marginBottom = style['margin-bottom'];
        }
        if ('padding-top' in style) {
            element.style.paddingTop = style['padding-top'];
        }
        if ('padding-bottom' in style) {
            element.style.paddingBottom = style['padding-bottom'];
        }
        if ('border-top' in style) {
            element.style.borderTop = style['border-top'];
        }
        if ('display' in style) {
            element.style.display = style['display'];
        }
        if ('min-width' in style) {
            element.style.minWidth = style['min-width'];
        }
        if ('min-height' in style) {
            element.style.minHeight = style['min-height'];
        }
        if ('color' in style) {
            element.style.color = style['color'];
        }
        if ('text-decoration' in style) {
            element.style.textDecoration = style['text-decoration'];
        }
        if ('font-size' in style) {
            element.style.fontSize = style['font-size'];
        }
        return element;
    }
    Private.apply_style = apply_style;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/utility.js":
/*!************************!*\
  !*** ./lib/utility.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "get_json_request_payload_from_file_list": () => (/* binding */ get_json_request_payload_from_file_list)
/* harmony export */ });
function get_json_request_payload_from_file_list(files) {
    const file_list = [];
    for (const f of files) {
        const entry = {
            path: f
        };
        file_list.push(entry);
    }
    return {
        files: file_list
    };
}


/***/ })

}]);
//# sourceMappingURL=lib_api_client_js-lib_index_js.353a412afd0654ff5bb8.js.map