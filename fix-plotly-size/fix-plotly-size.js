window.FixPlotlySize = {
  id: 'FixPlotlySize',
  init: function(Reveal) {
    if (!window.require || document.querySelectorAll('.plotly-graph-div').length === 0) {
      return;
    }
    require(['plotly'], function(Plotly) {
      // Trigger once on initial load
      document.querySelectorAll('.js-plotly-plot').forEach(plotlyDiv => {
        Plotly.Plots.resize(plotlyDiv);
      })

      function resizeCurSlide() {
        let curSlide = Reveal.getCurrentSlide();
        curSlide.querySelectorAll('.js-plotly-plot').forEach(plotlyDiv => {
          Plotly.Plots.resize(plotlyDiv);
        });
      }
      // Then trigger on every slide change, since panelsets sometimes change
      Reveal.addEventListener( 'slidechanged', event => {
        resizeCurSlide();
      });

      // Also listen to tabby changes, which are custom events called 'tabby'
      window.addEventListener('tabby', event => {
        resizeCurSlide();
      });
    });
  }
}
