import pluginReact from "eslint-plugin-react";
import pluginPrettier from "eslint-plugin-prettier";
import configPrettier from "eslint-config-prettier";
import parserBabel from "@babel/eslint-parser";

export default [
  {
    files: ["**/*.js", "**/*.jsx"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      parser: parserBabel,
      parserOptions: {
        requireConfigFile: false,
        babelOptions: {
          presets: ["@babel/preset-react"],
        },
      },
    },
    plugins: {
      react: pluginReact,
      prettier: pluginPrettier,
    },
    rules: {
      "react/react-in-jsx-scope": "off",
      "prettier/prettier": "error",
    },
  },
  configPrettier,
];
