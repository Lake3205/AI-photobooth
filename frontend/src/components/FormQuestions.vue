<script lang="ts" setup>
import {useFormService} from "@/services/formService";

const {questions} = useFormService();

function tacAmount(scale: [number, number]): number {
  return (scale[1] - (scale[0] - 1));
}

function tacMidpoint(scale: [number, number]): number {
  return Math.ceil(tacAmount(scale) / 2);
}

</script>

<template>
  <div v-for="(question, id) in questions" :key="id"
       class="p-4 sm:p-5 rounded-xl bg-white/5 border border-white/10 space-y-3 sm:space-y-4 hover:bg-white/10 transition">
    <label :for="id.toString()" class="font-semibold text-base sm:text-lg text-white block">{{
        question.question
      }}</label>

    <div v-if="question.type === 'scale'" class="relative pb-8 pt-2">
      <input
          :id="id.toString()"
          :max="question.scale ? question.scale[1] : 5"
          :min="question.scale ? question.scale[0] : 1"
          :name="id.toString()"
          :value="tacMidpoint(question.scale ? question.scale : [1,5])"
          class="range-slider w-full"
          required
          type="range"
      />
      <div class="flex w-full px-[7px] justify-between absolute top-8 left-0 z-10">
        <div v-for="index in tacAmount(question.scale ? question.scale : [1, 5])"
             :key="index" class="bg-white/50 w-px h-[8px] relative flex flex-col">
          <span class="text-xs sm:text-sm text-gray-300 absolute left-0 top-2 -translate-x-1/2 font-medium">{{
              index
            }}</span>
        </div>
      </div>
    </div>

    <div v-else-if="question.type === 'yes_no_explain'" class="space-y-3 sm:space-y-4">
      <div class="flex items-center gap-4 sm:gap-6">
        <label :for="id.toString() + '_yes'" class="flex items-center gap-2 sm:gap-3 cursor-pointer group">
          <input
              :id="id.toString() + '_yes'"
              :name="id.toString()"
              class="radio-custom"
              required
              type="radio"
              value="yes"
          />
          <span class="text-white group-hover:text-indigo-300 transition font-medium text-sm sm:text-base">Yes</span>
        </label>
        <label :for="id.toString() + '_no'" class="flex items-center gap-2 sm:gap-3 cursor-pointer group">
          <input
              :id="id.toString() + '_no'"
              :name="id.toString()"
              class="radio-custom"
              required
              type="radio"
              value="no"
          />
          <span class="text-white group-hover:text-indigo-300 transition font-medium text-sm sm:text-base">No</span>
        </label>
      </div>
      <div class="space-y-2">
        <label :for="id.toString() + '_explanation'" class="block text-sm font-medium text-gray-300">
          Please explain your choice:
        </label>
        <textarea
            :id="id.toString() + '_explanation'"
            :name="id.toString() + '_explanation'"
            class="textarea-base"
            placeholder="Type your explanation here..."
            rows="4"
        ></textarea>
      </div>
    </div>
  </div>
</template>