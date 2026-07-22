document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.event-check').forEach(function (checkbox) {
    var key = 'bcn2026-' + checkbox.dataset.key;
    var event = checkbox.closest('.event');

    if (localStorage.getItem(key) === '1') {
      checkbox.checked = true;
      event.classList.add('event--done');
    }

    checkbox.addEventListener('change', function () {
      if (checkbox.checked) {
        localStorage.setItem(key, '1');
        event.classList.add('event--done');
      } else {
        localStorage.removeItem(key);
        event.classList.remove('event--done');
      }
    });
  });

  document.querySelectorAll('.listen-btn').forEach(function (button) {
    button.addEventListener('click', function () {
      if (!('speechSynthesis' in window)) {
        return;
      }
      var textEl = button.closest('.guide-listen').querySelector('.listen-text');
      var text = textEl ? textEl.textContent.trim() : '';
      if (!text) {
        return;
      }
      window.speechSynthesis.cancel();
      var utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'it-IT';
      window.speechSynthesis.speak(utterance);
    });
  });
});
