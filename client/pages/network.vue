<template>
  <div class="section">
    <div class="container">
      <h1 class="title">Network</h1>
      <hr />
      <d3-network
        :net-nodes="nodesResult"
        :net-links="linksResult"
        :options="options"
      ></d3-network>
      {{ linksResult }}
      {{ nodesResult }}
    </div>
  </div>
</template>

<script>
import D3Network from 'vue-d3-network'
import { mapGetters } from 'vuex'

export default {
  components: {
    D3Network
  },
  computed: {
    ...mapGetters('job', ['results']),
    nodesResult() {
      const tmp = this.results['nodes'] || []
      return JSON.parse(JSON.stringify(tmp))
    },
    linksResult() {
      const tmp = this.results['links'] || []
      return JSON.parse(JSON.stringify(tmp))
    }
  },
  data() {
    return {
      nodes: [],
      links: [],
      options: {
        force: 3000,
        nodeSize: 30,
        fontSize: 30,
        nodeLabels: true,
        linkWidth: 1
      }
    }
  }
}
</script>
