import { generateQueryHook } from "../../api/api";
import { components } from "../../api/schemas";

export const useClothes = generateQueryHook(
  'clothes',
  generateQueryHook.api.path('/clothes/').method('get'),
);

export const useUploadClothes = generateQueryHook(
  'uploadClothes',
  generateQueryHook.api.path('/clothes/').method('post')
);

export const useInProgressClothes = generateQueryHook(
  'inProgressClothes',
  generateQueryHook.api.path('/clothes/in-progress').method('get')
);

export const useUpload = generateQueryHook(
  'upload',
  generateQueryHook.api.path('/uploads/{filename}').method('get')
);
