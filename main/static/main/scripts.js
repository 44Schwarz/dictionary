function addDictFunc() {
  let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  console.log($('#language1').val());

  $.ajax({
    type: "POST",
    url: '#',
    data: {csrfmiddlewaretoken: csrftoken, 'language1': $('#language1').val(), 'language2': $('#language2').val()},
    success: function (data) {
      if (data['created']) {
        let dict_id = data['dict_id'];
        let dict_name = data['dict_name'];

        $('#exists').hide();
        $('#listDict').append(`<a href="${dict_id}" class="list-group-item list-group-item-action">${dict_name}</a>`);
      }
      else {
        $('#exists').show();
      }
    }
  });
}

function addWordFunc() {
  let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

  $.ajax({
    type: "POST",
    url: "/dictionaries/add_word/",
    data: {csrfmiddlewaretoken: csrftoken, 'dict_id': $('#dict_id').val(), 'word': $('#word').val(), 'definition': $('#definition').val(), 'usage': $('#usage').val(), 'translation': $('#translation').val()},
    success: function (data) {
      if (data['done']) {
        location.reload();
      }
    }
  });
}

function editWordFunc() {
  let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

  $.ajax({
    type: "POST",
    url: "#",
    data: {csrfmiddlewaretoken: csrftoken, 'word_id': $('#idModal').val(), 'word': $('#wordModal').val(), 'definition': $('#defModal').val(), 'usage': $('#usgModal').val(), 'translation': $('#translModal').val()},
    success: function (data) {
      if (data['done']) {
        location.reload();
      }
    }
  });
}

function deleteWord() {
  let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

  $.ajax({
    type: "POST",
    url: "/dictionaries/delete_word/",
    data: {csrfmiddlewaretoken: csrftoken, 'word_id': $('#idModal').val()},
    success: function (data) {
      if (data['done']) {
        location.reload();
      }
    }
  });

}

function editModalPopulate(word, word_id, definition, usages, translation) {
    $('#wordModal').val(word);
    $('#defModal').val(definition);
    $('#usgModal').val(usages.join('\n'));
    $('#translModal').val(translation);

    $('#idModal').val(word_id);
}

