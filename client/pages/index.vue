<template>
  <div class="section">
    <div class="container">
      <h1 class="title">Doc Miner</h1>
      <hr />
      <div class="field">
        <div class="control">
          <textarea
            v-model="text"
            class="textarea"
            rows="25"
            placeholder="解析したいテキストを入力してください"
          ></textarea>
        </div>
      </div>
      <button class="button" @click="submit()">analyze</button>
      <button class="button" @click="submit2()">visualize</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: ''
    }
  },
  methods: {
    submit() {
      this.$store.dispatch('job/setText', this.text)
      this.$store.dispatch('job/postData')
    },
    submit2() {
      this.$store.dispatch('job/setText', this.text)
      this.$store.dispatch('job/postData2')
    }
  }
}
</script>

<style></style>
