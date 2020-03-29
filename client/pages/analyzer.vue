<template>
  <div class="columns">
    <div class="column is-3 setting-part">
      <div class="section">
        <p>固有表現ハイライト</p>
        <br />
        <div class="field">
          <input
            id="personCheck"
            type="checkbox"
            class="is-checkradio"
            v-model="isActive['PERSON']"
          />
          <label for="personCheck">PERSON</label>
        </div>
        <div class="field">
          <input
            id="orgCheck"
            class="is-checkradio"
            type="checkbox"
            v-model="isActive['ORG']"
          />
          <label for="orgCheck">ORG</label>
        </div>
        <hr />
        <p>重要文抽出</p>
        <br />
        <div class="field">
          <label>重要度 {{ topRank }} 位まで抽出</label>
          <input
            class="slider is-fullwidth"
            step="1"
            min="1"
            :max="maxRank"
            type="range"
            v-model="topRank"
          />
        </div>
        <div class="field">
          <input
            id="highlightCheck"
            class="is-checkradio"
            type="checkbox"
            v-model="showHighlight"
          />
          <label for="highlightCheck">ハイライト</label>
        </div>
        <div class="field">
          <input
            id="showAllCheck"
            class="is-checkradio"
            type="checkbox"
            v-model="showAllText"
          />
          <label for="showAllCheck">全文表示</label>
        </div>
      </div>
    </div>
    <div class="column doc-part">
      <button
        class="button is-small openButton"
        @click="showSidePanel = !showSidePanel"
        :class="{ open: showSidePanel }"
      >
        <span class="arrow">
          <i class="fas fa-angle-double-left"></i>
        </span>
      </button>
      <div class="section">
        <div
          class="sentence-part"
          v-for="sent in extractResults"
          :key="sent.id"
          :style="{
            background: 'rgba(237,194,95,' + calcAlpha(sent.rank) + ')'
          }"
        >
          <template v-for="token in sent.sent">
            <span
              class="token-part"
              :id="'ent' + token.id"
              :key="token.id"
              :class="{
                active: isActive[token.label],
                refered: isRefered[token.id]
              }"
              >{{ token.text }}</span
            >
            {{ ' ' }}
          </template>
        </div>
      </div>
    </div>
    <transition>
      <div class="column is-3 side-info" v-if="showSidePanel">
        <div class="section">
          <table class="table is-fullwidth">
            <tr>
              <th>Entity</th>
              <th>Label</th>
              <th>Move</th>
            </tr>
            <tr
              class="entity-part"
              v-for="token in extractEnts"
              :key="token.id"
              @mouseover="updateIsRefer(token.id, true)"
              @mouseleave="updateIsRefer(token.id, false)"
            >
              <td>{{ token.text }}</td>
              <td>{{ token.label }}</td>
              <td>
                <nuxt-link v-scroll-to="'span#ent' + token.id" to
                  >click</nuxt-link
                >
              </td>
            </tr>
          </table>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters('job', ['results']),
    maxRank() {
      const results = this.$store.state.job.results
      return Math.max.apply(
        null,
        results.map(x => x['rank'])
      )
    },
    extractResults() {
      const results = this.$store.state.job.results
      return results.filter(x => {
        return x['rank'] <= this.topRank || this.showAllText == true
      })
    },
    extractEnts() {
      let ents = this.extractResults.map(x => x['sent'])
      ents = ents.reduce((a, c) => {
        return a.concat(c)
      })
      return ents.filter(x => {
        return x.label != 'O'
      })
    }
  },
  data() {
    return {
      isActive: {
        PERRSON: false,
        ORG: false
      },
      isRefered: {},
      topRank: 3,
      showAllText: false,
      showHighlight: true,
      showSidePanel: false
    }
  },
  methods: {
    calcAlpha(rank) {
      if (this.showHighlight && rank <= this.topRank) {
        return (this.maxRank - rank) / this.maxRank
      } else {
        return 0
      }
    },
    updateIsRefer(id, val) {
      this.$set(this.isRefered, id, val)
    }
  }
}
</script>

<style>
.sentence-part {
  padding: 2px 5px;
  margin-bottom: 1px;
}

.active {
  background: lightyellow;
}

.refered {
  background: lightpink;
}

div.doc-part {
  height: 100vh;
  overflow: auto;
}
div.setting-part {
  height: 100vh;
  overflow: auto;
  box-shadow: 5px 0px 5px #999;
}

.side-info {
  height: 100vh;
  box-shadow: -3px 0px 1px #999;
  overflow: auto;
  background: rgb(248, 248, 248);
}

.entity-part:hover {
  background: lightpink;
}

.openButton {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 100;
  box-shadow: 3px 3px 3px #999;
}

.openButton.open .arrow {
  transform: rotate(180deg);
}

.arrow {
  transition: 0.5s;
}

.v-enter-active,
.v-leave-active {
  transform: translate(0px, 0px);
  transition-timing-function: ease-in-out;
  transition-duration: 0.5s;
}

.v-enter,
.v-leave-to {
  transform: translateX(100vw) translateX(0px);
  transition-timing-function: ease-in-out;
  transition-duration: 0.5s;
}
</style>
