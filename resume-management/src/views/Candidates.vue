<template>
  <div class="candidates-view">
    <CandidateList ref="candidateList"/>
  </div>
</template>

<script>
import CandidateList from '../components/CandidateList.vue';

export default {
  name: 'Candidates',
  components: {
    CandidateList
  }
};
</script>

<style scoped>
.candidates-view {
  width: 100%;
}
</style>

