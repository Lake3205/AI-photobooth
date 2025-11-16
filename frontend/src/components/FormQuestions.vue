<script lang="ts" setup>
import { useFormService } from "@/services/formService";

const { questions } = useFormService();

function tacAmount(scale: [number, number]): number {
  return (scale[1] - (scale[0] - 1));
}

function tacMidpoint(scale: [number, number]): number {
  return Math.ceil(tacAmount(scale) / 2);
}

</script>

<template>
  <div v-for="(question, id) in questions" :key="id">
    <label :for="id.toString()" class="font-medium text-lg">{{ question.question }}</label>
    <div v-if="question.type === 'scale'" class="relative pb-5">
        <input
          type="range"
          :id="id.toString()"
          :name="id.toString()"
          :min="question.scale ? question.scale[0] : 1"
          :max="question.scale ? question.scale[1] : 5"
          :value="tacMidpoint(question.scale ? question.scale : [1,5])"
          required
          class="w-full z-20 relative"
        />
        <div class="flex w-full px-[7px] justify-between absolute top-5 left-0 z-10">
            <div class="bg-[#fff] opacity-75 w-px h-[6px] left-0 relative flex flex-col" v-for="index in tacAmount(question.scale ? question.scale : [1, 5])" :key="index">
                <span class="text-[0.8rem] absolute left-0 top-1 -translate-x-1/2">{{ index }}</span>
            </div>
        </div>
    </div>
    <div v-else-if="question.type === 'yes_no_explain'" class="flex flex-col gap-2">
        <div class="flex items-center gap-4">
            <label :for="id.toString() + '_yes'" class="flex items-center gap-2 cursor-pointer">
                <input type="radio" :id="id.toString() + '_yes'" :name="id.toString()" value="yes" required />
                <span>Yes</span>
            </label>
            <label :for="id.toString() + '_no'" class="flex items-center gap-2 cursor-pointer">
                <input type="radio" :id="id.toString() + '_no'" :name="id.toString()" value="no" required />
                <span>No</span>
            </label>
        </div>
        <div>
            <label :for="id.toString() + '_explanation'" class="block font-medium mb-1">Please explain your choice:</label>
            <textarea
                :id="id.toString() + '_explanation'"
                :name="id.toString() + '_explanation'"
                rows="4"
                class="w-full min-h-[42px] rounded-md border border-gray-300 bg-white/10 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            ></textarea>
        </div>
    </div>
  </div>
</template>

<style scoped>
::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #04AA6D;
  cursor: pointer;
}

::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #04AA6D;
  cursor: pointer;
}
</style>