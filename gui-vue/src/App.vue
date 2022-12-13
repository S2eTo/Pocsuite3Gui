<template>
  <div id="app">
    <div class="bl title">
      <div class="left">Pocsuite3 可视化</div>
      <div class="right">远程漏洞测试和概念验证框架</div>
    </div>
    <div class="bl l-title">
      <div class="left">功能列表</div>
      <div class="right">
        <el-link size="small" plain icon="el-icon-arrow-left" v-if="show_back" @click="back"
                 :underline="false">
          返回
        </el-link>
        <span style="margin-left: 15px">{{ title.toLowerCase() == 'home' ? "首页" : title }}</span>
      </div>
    </div>
    <div class="bl container">
      <div class="left nav-list">
        <div class="nav-list_item" v-for="(data, index) in menu" :key="index" @click="navigator_to(data.href)">
          {{ data.link }}
        </div>
      </div>
      <div class="right content">
        <router-view/>
      </div>
    </div>
    <div class="btools">
      <div id="tz" @mousedown="dragEagle"></div>
      <div class="btools-content console" v-if="show_console">
        <div class="title">
          <div class="btools-content-title-left">Console</div>
          <div class="btools-content-title-right">
            <div class="close" @click="switch_console">-</div>
          </div>
        </div>
        <div class="btools-auto-container">
          <div :class="'log' + ' ' +logger_levelcss(data.levelno, data.levelname)" v-for="(data, index) in logger"
               :key="index">
            <div v-if="data.levelno == -1">
              <br/>
              <span class="msg">{{ data.msg }}</span>
            </div>
            <div v-else-if="data.levelno == -2">
              <pre class="msg"><code style="color: var(--logger-error);">{{ data.msg.trim() }}</code></pre>
            </div>
            <div v-else-if="data.levelno == -3">
              <br/>
              <pre><code class="msg">{{ data.msg.trim() }}</code></pre>
            </div>
            <div v-else>
              <span class="strftime">[{{ data.strftime }}]</span> <span class="levelname">[{{ data.levelname }}]</span>&nbsp;<span
                class="msg">{{ data.msg }}</span>
            </div>
          </div>

        </div>
      </div>
      <div class="btools-list">
        <div class="btools-list--item" @click="switch_console"><i class="el-icon-cpu"></i>console</div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      title: "home",
      show_back: false,
      logger: [],
      btools: {},
      show_console: true,
      menu: [
        {"href": 'home', "link": "Poc 列表"},
        // {"href": 'variables', "link": "公共参数"},
      ]
    }
  },
  created: function () {
    let self = this;
    this.channels.$on("switch_page", function (t, s = false) {
      self.title = t;
      self.show_back = s;
    })

    this.channels.$on("show_console", function () {
      self.show_console = true;
    })

    setTimeout(function () {
      self.init();
    }, 1)

    window.socketio.on("connect", function () {
      self.logger = JSON.parse(localStorage.getItem("logger"))
      self.scroll_to_bottom();
    })

    window.socketio.on('message', function (res) {
      if (res.action == "logger") {
        self.logger.push(res.data);
        localStorage.setItem("logger", JSON.stringify(self.logger))
        self.scroll_to_bottom();
      } else if (res.action == "clear_logger") {
        self.clear_logger()
      } else {
        console.log(res)
      }
    });
  },
  methods: {
    init: function () {
      let navlist = document.querySelector(".left.nav-list");
      let content = document.querySelector(".right.content");

      content.setAttribute("style", `height: ${window.innerHeight - 135}px`)
      navlist.setAttribute("style", `height: ${window.innerHeight - 105}px`)
    },
    scroll_to_bottom: function () {
      setTimeout(function () {
        let element = document.querySelector(".btools-auto-container")
        element.scrollTo(0, element.scrollHeight)
      }, 1)
    },
    clear_logger() {
      this.logger = []
      localStorage.setItem("logger", "[]")
    },
    navigator_to: function (t) {
      this.title = t
      this.$router.push({name: t})
    },
    back: function () {
      this.$router.push({name: 'home'})
      this.title = "home"
      this.show_back = false;
    },
    logger_levelcss: function (levelno, levelname) {
      levelname = levelname.toString()

      let class_name = null
      if (levelname == "INFO") {
        class_name = "sysinfo"
      } else if (levelname == "ERROR") {
        class_name = "sysinfo"
      } else if (levelname == "WARNING") {
        class_name = "warning"
      }

      if (class_name != null) return class_name

      levelno = parseInt(levelno)
      if (levelno == 21) {
        return "sysinfo_no"
      } else if (levelno == 22) {
        return "success_no"
      } else if (levelno == 23) {
        return "error_no"
      } else if (levelno == 24) {
        return "warning_no"
      }
    },
    switch_console: function () {
      this.show_console = !this.show_console
    },
    dragEagle: function (event) {
      let targetDiv = document.querySelector('.btools-auto-container');
      let targetDivHeight = targetDiv.offsetHeight;
      let startY = event.clientY;
      let self = this;
      document.onmousemove = function (e) {
        e.preventDefault();
        let dstY = Math.abs(e.clientY - startY);

        if (e.clientY < startY) {
          targetDiv.style.height = targetDivHeight + dstY + 'px';
        }

        if (e.clientY > startY) {
          targetDiv.style.height = (targetDivHeight - dstY) + 'px';
        }

        if (parseInt(targetDiv.style.height) <= 10) {
          self.show_console = false
        }
      }
      document.onmouseup = function () {
        document.onmousemove = null;
      }
    }
  },
};
</script>


<style>
:root {
  --left-width: 200px;
  --bl-padding: 15px 20px;
  --logger-success: #6fc587;
  --logger-error: hsl(6deg 84% 66%);
  --logger-info: #b1c7e2;
  --logger-warning: #ffea7f;
}

* {
  font-family: "Consolas", "Lucida Console";
  margin: 0;
  padding: 0;
  font-size: 14px;
  box-sizing: border-box;
}

body {
  background: #F2F6FC;
}


.bl {
  position: relative;
  vertical-align: top;
}

.title .right,
.title .left {
  color: #fff;
  font-size: 17px;
}

.title .left {
  background: #4d79dc;
  font-weight: bold;
}

.title .right {
  background: #5a8cff;
}

.l-title .left,
.l-title .right {
  background: #ffffff;
}

.l-title .left {
  border-right: 1px solid #f1f1f1;
  border-bottom: 1px solid #f1f1f1;
}

.bl .left,
.bl .right {
  padding: var(--bl-padding);
  display: inline-block;
  vertical-align: middle;
}

.bl .left {
  width: var(--left-width);
}

.bl .right {
  width: calc(100% - var(--left-width));
}

.nav-list {
  position: absolute;
  height: 100%;
  background: #ffffff;
}

.nav-list .nav-list_item {
  cursor: pointer;
  user-select: none;
  padding: 8px 20px;
  border-radius: 25px;
  font-size: 14px;
}

.right.content {
  margin-top: 30px;
  padding: 0 40px 30px 40px;
  overflow: auto;
  margin-left: var(--left-width);
}

.btools {
  position: absolute;
  bottom: 0;
  left: 0;
  z-index: 999;
  width: 100%;
}

.btools #tz {
  border-top: 2px solid #ebebeb;
}

.btools #tz:hover {
  cursor: n-resize;
}

.btools .btools-list {
  text-align: right;
  background: #ffffff;
}

.btools .btools-list .btools-list--item {
  padding: 3px 10px;
  display: inline-block;
  cursor: pointer;
  user-select: none;
}

.btools .btools-list .btools-list--item i {
  vertical-align: middle;
  margin-right: 2px;
}

.btools .btools-list .btools-list--item i.el-icon-cpu {
  color: #4d79dc;
}

.btools .btools-list .btools-list--item:hover {
  background: #d7d7d7;
}

.btools-content .btools-auto-container {
  height: 300px;
  width: 100%;
  overflow: auto;
}

.btools-content .btools-auto-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.btools-content .btools-auto-container::-webkit-scrollbar-thumb {
  background-color: #c46c5d;
  border-radius: 30px;
}

.btools-content .btools-auto-container::-webkit-scrollbar-track {
  background-color: #24292e;
}

.btools-content .title {
  background: #2f363d;
}

.btools-content .title .btools-content-title-left,
.btools-content .title .btools-content-title-right {
  width: 50%;
  display: inline-block;
  vertical-align: middle;
}

.btools-content .title .btools-content-title-left {
  text-align: left;
  padding: 5px 10px;
}

.btools-content .title .btools-content-title-right {
  text-align: right;
}

.btools-content .title .close {
  display: inline-block;
  padding: 5px 10px;
  user-select: none;
  font-weight: bold;
  font-size: 20px;
  cursor: pointer;
}


.btools-content .title .close:hover {
  background: #2f363d;
}

.console {
  z-index: 99;
  background: #24292e;
  width: 100%;
}


.console * {
  color: #ffffff;
}

.console .log {
  padding: 3px 5px;
}

.console .log.sysinfo_no *,
.console .log .strftime {
  color: var(--logger-info);
}

.console .log.success_no *,
.console .log.sysinfo .levelname {
  color: var(--logger-success);
}

.console .log.error_no *,
.console .log.error .levelname {
  color: var(--logger-error);
}

.console .log.warning_no *,
.console .log.warning .levelname {
  color: var(--logger-warning);
}
</style>
