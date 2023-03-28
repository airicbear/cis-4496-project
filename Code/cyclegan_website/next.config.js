
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    reactStrictMode: true,
    webpack: (config, { }) => {

        config.resolve.extensions.push(".ts", ".tsx");
        config.resolve.fallback = { fs: false };

        config.plugins.push(
            new CopyPlugin({
                patterns: [
                    {
                        from: './node_modules/onnxruntime-web/dist/ort-wasm.wasm',
                        to: 'static/chunks',
                    },
                    {
                        from: './node_modules/onnxruntime-web/dist/ort-wasm-simd.wasm',
                        to: 'static/chunks',
                    },
                    {
                        from: './node_modules/onnxruntime-web/dist/ort-wasm.wasm',
                        to: 'static/chunks/pages/generators',
                    }, {
                        from: './node_modules/onnxruntime-web/dist/ort-wasm-simd.wasm',
                        to: 'static/chunks/pages/generators',
                    },
                ],
            }),
        );

        return config;
    }
}