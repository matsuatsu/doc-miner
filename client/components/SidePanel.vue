<template>
  <div class="side-info-part">
    <div class="section">
      test
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style>
.side-info-part {
  position: fixed;
  top: 0px;
  left: 80%;
  width: 20%;
  height: 100vh;
  /* z-index: 100; */
  box-shadow: -3px 0px 1px #999;
  overflow: auto;
  background: rgb(245, 245, 245);
}
</style>
