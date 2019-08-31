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
    // process: './classify',
    process: 'https://asia-east2-cs-currency-classifier.cloudfunctions.net/classifier',
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
  let prediction = document.querySelector(`#prediction`);
  let outputTable = document.querySelector(`#output`);
  let classCount = 2;
  prediction.innerHTML = 'Prediction: '
  for (i = 0; i < classCount; i++) {
    outputTable.rows[i + 1].cells[1].innerHTML = '';
    outputTable.rows[i + 1].classList.remove('is-selected');
  }
  if (error === null) {
    let data = JSON.parse(file.serverId);
    // console.log(data);


    prediction.innerHTML = 'Prediction: ' + data[1].toString();
    max = data[2][0];
    max_index = 0;
    for (i = 0; i < data[2].length; i++) {
      outputTable.rows[i + 1].cells[1].innerHTML = data[2][i].toString();
      outputTable.rows[i + 1].classList.remove('is-selected');
      if (data[2][i] > max) {
        max = data[2][i];
        max_index = i;
      }

    }
    outputTable.rows[max_index + 1].classList.add('is-selected');
  }
});

// pond.on("removefile", (error, file) => {
//   if (error === null && !replaced) {
//     document.getElementById('photo').setAttribute('src', 'https://via.placeholder.com/400x250/jpg');
//   }
//   replaced = false;
// });
