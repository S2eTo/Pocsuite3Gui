import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import socket from 'socket.io-client';
window.socketio = socket("http://127.0.0.1:8888/ws")
Vue.prototype.channels = new Vue();

Vue.use(ElementUI);
Vue.config.productionTip = false

String.prototype.rsplit = function(sep, maxsplit) {
  let split = this.split(sep);
  return maxsplit ? [ split.slice(0, -maxsplit).join(sep) ].concat(split.slice(-maxsplit)) : split;
}
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
