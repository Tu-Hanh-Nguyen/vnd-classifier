// Copyright 2018 Google LLC.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Script for configuring FilePond, a file upload library.
// See https://github.com/pqina/filepond for more information.

FilePond.setOptions({
  instantUpload: false,
  allowMultiple: false,
  allowImagePreview: false,
  allowDrop: false,
  allowBrowse: false,
  allowReplace: true,
  labelIdle: 'File to upload',
  server: {
    process: './classify',
    // "https://asia-east2-cloud-next-demo-242611.cloudfunctions.net/upload_image",
    fetch: null,
    revert: null,
    restore: null,
    load: null
  }
});
// FilePond.registerPlugin(FilePondPluginImagePreview);
const pond = FilePond.create(document.querySelector('input[type="file"]'));
var replaced = false;
pond.on("processfile", (error, file) => {
  if (error === null) {
    let id = file.serverId;
    console.log(id);
    // let uploadFileIdInputNode = document.querySelector(`#image`);
    // uploadFileIdInputNode.value = id;
  }
});

pond.on("removefile", (error, file) => {
  if (error === null && !replaced) {
    document.getElementById('photo').setAttribute('src', 'https://via.placeholder.com/400x300/jpg');
  }
  replaced = false;
});

var canvas = document.getElementById('canvas');
document.getElementById('capture').addEventListener('click', function () {
  canvas.toBlob(function (blob) {
    pond.addFile(blob);
    replaced = true;
  }, 'image/jpeg');
});
