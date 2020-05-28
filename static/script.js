// $(function(){
//   $('.button').on("click", function(){
//     if($('body').hasClass('nav_is_visible') == true){
//      $('body').removeClass('nav_is_visible');
//      $('.button').removeClass('close');
//         }
//     else{
//      $('body').addClass('nav_is_visible');
//      $('.button').addClass('close');
//        }
//    });
  
//   $('body').addClass('home_is_visible');

    
//  function removeClasses() {
//   $(".menu ul li").each(function() {
//     var custom_class = $(this).find('a').data('class');
//   $('body').removeClass(custom_class);
//   });
// }
  
//   $('.menu a').on('click',function(e){
//     e.preventDefault();
//     removeClasses();
//     var custom_class = $(this).data('class');
//     $('body').addClass(custom_class);
//   });
// });

(function() {
   
  'use strict';
 
  $('.input-file').each(function() {
    var $input = $(this),
        $label = $input.next('.js-labelFile'),
        labelVal = $label.html();
     
   $input.on('change', function(element) {
      var fileName = '';
      if (element.target.value) fileName = element.target.value.split('\\').pop();
      fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
   });
  });
 
})();

/* Открытие меню */
var main = function() { //главная функция
  $('.icon-menu').click(function() { //выбираем класс icon-menu и добавляем метод click с функцией, вызываемой при клике
      $('.menu').animate({ //выбираем класс menu и метод animate
          left: '0px' //теперь при клике по иконке, меню, скрытое за левой границей на 285px, изменит свое положение на 0px и станет видимым
      }, 200); //скорость движения меню в мс
      
      $('body').animate({ //выбираем тег body и метод animate
          left: '285px' //чтобы всё содержимое также сдвигалось вправо при открытии меню, установим ему положение 285px
      }, 200); //скорость движения меню в мс
  });


/* Закрытие меню */
  $('.icon-close').click(function() { //выбираем класс icon-close и метод click
      $('.menu').animate({ //выбираем класс menu и метод animate
          left: '-285px' //при клике на крестик меню вернется назад в свое положение и скроется
      }, 200); //скорость движения меню в мс
      
  $('body').animate({ //выбираем тег body и метод animate
          left: '0px' //а содержимое страницы снова вернется в положение 0px
      }, 200); //скорость движения меню в мс
  });
};

$(document).ready(main); //как только страница полностью загрузится, будет вызвана функция main, отвечающая за работу меню
