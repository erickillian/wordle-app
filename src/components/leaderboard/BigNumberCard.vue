<template>
    <v-card 
        v-if="loading == false"
    >
        <v-card-text class="subtitle-1 text-center pb-0">
            {{ title }}
        </v-card-text>
        <v-card-text class="display-2 pt-0 font-weight-bold text-center text--darken-3">
            {{ value }}
        </v-card-text>
    </v-card>
</template>

<script>
export default {
  props: {
    title: String,
    value: Number,
    loading: Boolean,
  }
}
</script>
