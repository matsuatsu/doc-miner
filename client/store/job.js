import axios from 'axios'

export const state = () => ({
  text: '',
  results: []
})

export const getters = {
  results: state => state.results
}

export const mutations = {
  setText(state, text) {
    state.text = text
  },
  setResults(state, results) {
    state.results = results
  }
}

export const actions = {
  setText({ commit }, text) {
    commit('setText', text)
  },
  async postData({ state, commit }) {
    const data = new FormData()
    data.append('text', state.text)
    const response = await axios.post('http://localhost:8080/api/ner', data)
    commit('setResults', response['data'])
    console.log(response)
    this.$router.push('/analyzer')
  }
}
