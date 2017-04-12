// Copyright 2016 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

Shader "Brush/Special/Unlit" {

Properties {
    _MainTex ("Texture", 2D) = "white" {}
    _Cutoff ("Alpha cutoff", Range(0,1)) = 0.5
    _NoiseTex ("NoiseTex (R)",2D) = "white"{}
    _DissolveSpeed ("DissolveSpeed (Second)",Float) = 10
    _EdgeWidth("EdgeWidth",Range(0,0.5)) = 0.1
    _EdgeColor("EdgeColor",Color) =  (1,1,1,1)
}

SubShader {
    Pass {
        Tags {"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
        Lighting Off
        Cull Off

        CGPROGRAM

        #pragma vertex vert
        #pragma fragment frag
		#include "../../../Shaders/Brush.cginc"
        #include "UnityCG.cginc"

        sampler2D _MainTex;
        float _Cutoff;
        uniform sampler2D _NoiseTex;
        uniform float _DissolveSpeed;
        uniform float _EdgeWidth;
        uniform float4 _EdgeColor;

        struct appdata_t {
            float4 vertex : POSITION;
            float2 texcoord : TEXCOORD0;
            float4 color : COLOR;
        };

        struct v2f {
            float4 vertex : POSITION;
            float2 texcoord : TEXCOORD0;
            float4 color : COLOR;
        };

        v2f vert (appdata_t v)
        {

            v2f o;
			
            o.vertex = mul(UNITY_MATRIX_MVP, v.vertex);
            o.texcoord = v.texcoord;
            o.color = v.color;
            return o;
        }

        fixed4 frag (v2f i) : COLOR
        {
            float DissolveFactor = saturate(_Time.y / _DissolveSpeed);
            float noiseValue = tex2D(_NoiseTex, i.texcoord).r;
            if(noiseValue <= DissolveFactor) {
                discard;
            }

            fixed4 texColor = tex2D(_MainTex, i.texcoord) * i.color;
            // float4 texColor = tex2D(_MainTex, i.uv);
            if (texColor.a < _Cutoff) {
                discard;
            }
            texColor.a = 1;
            float EdgeFactor = saturate((noiseValue - DissolveFactor)/(_EdgeWidth*DissolveFactor));
            float4 BlendColor = texColor * _EdgeColor;

            return lerp(texColor, BlendColor, 1 - EdgeFactor);
            // return texColor;              

        }

        ENDCG
    }
}

 Fallback "Unlit/Diffuse"
//Fallback off

}
