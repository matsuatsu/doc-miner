import Vue from 'vue'
import VueScrollTo from 'vue-scrollto'

Vue.use(VueScrollTo, {
  container: '.doc-part',
  duration: 600,
  easing: 'ease-in-out',
  offset: -100
})
