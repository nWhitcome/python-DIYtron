const KnobHelper = {};
(function(undefined) {

  const members = {

    /*
    ---------------------------------------------------------------------------
      CSS Knob Creation and Drawing Functions
    ---------------------------------------------------------------------------
    */

    createKnobCSS: function(inputEl, containerClass, text) {
      const knob = new Knob(inputEl,
          function(knob, indicator) {
            KnobHelper.drawKnobCSS(knob, indicator);
          }),
          $input     = $(knob.element),
          $container = $(`<div class="ui-knob-container ${containerClass}">`),
          $text      = $(`<div class="knob-text-box">${text}</div>`);
          $body      = $('<div class="ui-knob ui-knob-shadow">'),
          $indicator = $('<div class="ui-knob-indicator">');


      $container.append($body);
      $container.append($indicator);

      $input.hide();
      $container.insertBefore($input);
      $container.append($input);
      $container.append($text);

      // center knob in container
      $body.css({
        "margin-top": -($body.outerHeight()/2),
        "margin-left":-($body.outerWidth()/2)
      });

      setupKnob(knob, $container[0]);

      return knob;

    },

    drawKnobCSS: function(knob, indicator) {
      const $indicator = $(knob.element).siblings('.ui-knob-indicator');
      $indicator.css({
        left: indicator.x - $indicator.outerWidth()/2,
        top:  indicator.y - $indicator.outerHeight()/2 - 20
      });

      const rotateText = `rotate(${(-indicator.angle)}deg)`;
      $indicator.css({
        'transform': rotateText,
        '-webkit-transform': rotateText,
        '-moz-transform': rotateText,
        '-o-transform': rotateText
      });
    },

  } // end members

  for (const key in members) {
    KnobHelper[key] = members[key];
  }
})();