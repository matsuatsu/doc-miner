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
          <input id="orgCheck" class="is-checkradio" type="checkbox" v-model="isActive['ORG']" />
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
          <input id="highlightCheck" class="is-checkradio" type="checkbox" v-model="showHighlight" />
          <label for="highlightCheck">ハイライト</label>
        </div>
        <div class="field">
          <input id="showAllCheck" class="is-checkradio" type="checkbox" v-model="showAllText" />
          <label for="showAllCheck">全文表示</label>
        </div>
        <button class="button" @click="showSidePanel = !showSidePanel">show side info</button>
      </div>
    </div>
    <div class="column doc-part">
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
              :key="token.id"
              :class="{ active: isActive[token.label] }"
            >{{ token.text }}</span>
            {{ ' ' }}
          </template>
        </div>
      </div>
    </div>
    <div class="column is-2 side-info" v-if="showSidePanel">
      <div class="section">test</div>
    </div>
    <div class="side-info-menu" v-else>
      <span class="vertical">固有表現一覧</span>
    </div>
    <!-- <SidePanel></SidePanel> -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SidePanel from '~/components/SidePanel.vue'

export default {
  components: {
    SidePanel
  },
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
    }
  },
  data() {
    return {
      isActive: {
        PERRSON: false,
        ORG: false
      },
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
  background: rgb(245, 245, 245);
}
.side-info-menu {
  width: 40px;
  height: 100vh;
  box-shadow: -3px 0px 1px #999;
  overflow: auto;
  background: rgb(245, 245, 245);
}

.vertical {
  writing-mode: vertical-rl;
}
</style>
