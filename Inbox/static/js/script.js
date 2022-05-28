 /*==================
  # ВСЕ СКРИПТЫ ЗДЕСЬ
  БУДУТ ОТОБРАЖАТЬСЯ
  НА СТРАНИЦЕ
===================== */

  // Cчетчик оставшихся символов
  $(document).ready(function() {
    var start = 0;
    var limit = 1000;

    $('#message').keyup(function () {
      start = this.value.length
      if (start > limit) {
        return false;
      }

      else if(start == 1000){
        $("#remaining").html("Characters remaining: " + (limit - start)).css('color', 'red');
        swal("Opsss !", "Лимит символов исчерпан !", "info");
      }

      else if(start > 984){
        $("#remaining").html("Characters remaining: " + (limit - start)).css('color', 'red');
      }

      else if(start < 1000){
        $("#remaining").html("Characters remaining: " + (limit - start)).css('color', 'black');
      }

      else {
        $("#remaining").html("Characters remaining: " + (limit)).css('color', 'black');
      }
    });
  })

   // InputMask(Телефон)
   $(document).ready(function() {
     $('.phone').inputmask("(99) 99999-9999", {"onincomplete": function(){
       swal("Opsss !", "Неполный данные телефона. Пожалуйста проверьте !", "info");
       $('.phone').val("");
       return false;
     }})
   })

   // Получение(Время)
   setInterval(function() {
    var date = new Date();
     $('#clock').html(
       (date.getHours() < 10 ? '0' : '') + date.getHours() + ':' +
       (date.getMinutes() < 10 ? '0' : '') + date.getMinutes() + ':' +
       (date.getSeconds() < 10 ? '0' : '') + date.getSeconds()
     );
   }, 500);

   // Обновление страницы всегда в (0:00)
   function autoRefresh(hours, minutes, seconds) {
     var now = new Date(), then=new Date();
     then.setHours(hours, minutes, seconds, 0);
     if(then.getTime() < now.getTime()){
     t]\'zq x c[\qwe [rcwe rvb5hen.setDate(now.getDate() + 1);
    }
    var timeout=(then.getTime() - now.getTime());
    setTimeout(function(){
      window.location.reload(true);
    }, timeout())
  }
  autoRefresh(0,0,0)

   // Спрятать контент если нет сообщений
   $(document).ready(function() {
     var verify = $('#chk_td').length;
      if (verify==0){
        $('.hide').css('display', 'none');
        $('#msg').text('Не одного соощения не найдено');
        $('#refresh').html('<i class="fas fa-sync-alt fa-3x">');
      }
  });

  // Предупреждение пользователей за 5 минут(после 25 мин)
    setTimeout(function(){
        var notice = document.querySelector('#warning');
        if (notice){
          notice.click();
        }
      }, 1 * 10000); // 25 мин

    // Auto logout (после 5 мин)
      setTimeout(function(){
        var action = document.querySelector('#info');
        if (action){
          action.click();
        }
      }, 1 * 15000); // 30 мин
