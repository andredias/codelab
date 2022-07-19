<template lang="pug">
.documentation.miolo
    h1 {{ i18n.$t('terms_of_use') }}
    div(v-show="i18n.locale.value === 'pt-BR'")
        ol
            li
                div
                    | O serviço é prestado "COMO ESTÁ", sem qualquer tipo de garantia, expressa ou implícita, incluindo, mas não limitado às garantias de comercialização, adequação a um propósito e não-infração. Em nenhum caso o
                    |
                    b Code Lab
                    |
                    | ou algum de seus licenciadores será responsável por qualquer reivindicação, dano ou outra responsabilidade, seja em uma ação de contrato, ato ilícito ou de outra forma, resultantes do uso do serviço.
            li
                div
                    | O
                    |
                    b Code Lab
                    |
                    | e seus licenciadores renunciam quaisquer garantias relativas à segurança, confiabilidade, pontualidade e desempenho dos serviços. Também renunciam quaisquer garantias para qualquer informação, conteúdo ou conselhos obtidos através dos serviços.
            li
                div
                    | O
                    |
                    b Code Lab
                    |
                    | não se responsabiliza pelo conteúdo publicado pelos usuários e pelo conteúdo dos comentários publicados no site.
            li
                div
                    | Ao enviar, postar ou exibir conteúdo no site do
                    |
                    b Code Lab
                    |
                    | , você concede ao
                    |
                    b Code Lab
                    |
                    | e a outros usuários dos serviços uma licença mundial, não-exclusiva, livre de royalties (com o direito de sublicenciar) para usar, copiar, reproduzir, processar, adaptar, modificar, publicar, transmitir, exibir e distribuir esse conteúdo em toda e qualquer mídia ou métodos de distribuição (agora conhecida ou desenvolvida posteriormente). Especificamente, seguindo a
                    |
                    a(href="https://opensource.org/licenses/MIT") licença MIT
                    | .
            li
                div
                    | Você é responsável por seu uso do serviço
                    |
                    b Code Lab
                    | , por qualquer conteúdo por você fornecido, e por todas as consequências, incluindo o uso de seu conteúdo por outros usuários e parceiros de terceiros. Você entende que o seu conteúdo pode ser republicado e se você não tem o direito de enviar conteúdo para tal uso, pode sujeitá-lo à responsabilidade. O
                    |
                    b Code Lab
                    |
                    | não será responsável por qualquer uso de seu conteúdo, de acordo com estes Termos de Uso.
            li
                div
                    | No decurso da utilização do site do
                    |
                    b Code Lab
                    | , você pode fornecer comentários relativos (mas não limitadas) a sugestões, observações, erros, problemas e defeitos em relação ao site do
                    |
                    b Code Lab
                    | . Você concede ao
                    |
                    b Code Lab
                    |
                    | uma licença mundial, perpétua, irrevogável, livre de royalties transferível e sub-licenciável, não exclusiva para usar, copiar, modificar, distribuir, exibir, executar, criar trabalhos derivados e de outro modo explorar todos esses comentários.

    div(v-show="i18n.locale.value === 'en'")
        ol
            li
                div
                    | The service is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall
                    |
                    b Code Lab
                    |
                    | or its licensors be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the service or the use or other dealings in the service.
            li
                div
                    b Code Lab
                    |
                    | and its licensors disclaim any warranties regarding the security, reliability, timeliness, and performance of the services.
                    |
                    b Code Lab
                    |
                    | and its licensors disclaim, any warranties for any information, content or advice obtained through the services.
            li
                div
                    b Code Lab
                    |
                    | takes no responsibility for the content published by users, and for the content of comments they post on the
                    |
                    b Code Lab
                    |
                    | site.
            li
                div
                    | By submitting, posting or displaying content on the
                    |
                    b Code Lab
                    |
                    | Site, you grant
                    |
                    b Code Lab
                    |
                    | and other users of the Services a worldwide, non-exclusive, royalty-free license (with the right to sublicense) to use, copy, reproduce, process, adapt, modify, publish, transmit, display and distribute such Content in any and all media or distribution methods (now known or later developed). Specifically, the
                    |
                    a(href="https://opensource.org/licenses/MIT") MIT license
                    | .
            li
                div
                    | You are responsible for your use of the
                    |
                    b Code Lab
                    |
                    | service, for any content you provide, and for any consequences thereof, including the use of your content by other users and third party partners. You understand that your content may be republished and if you do not have the right to submit content for such use, it may subject you to liability.
                    |
                    b Code Lab
                    |
                    | will not be responsible or liable for any use of your Content in accordance with these Terms of Use.
            li
                div
                    | In the course of using the
                    |
                    b Code Lab
                    |
                    | Site, you may provide
                    |
                    b Code Lab
                    |
                    | with feedback, including but not limited to suggestions, observations, errors, problems, and defects regarding the
                    |
                    b Code Lab
                    |
                    | Site. You hereby grant
                    |
                    b Code Lab
                    |
                    | a worldwide, irrevocable, perpetual, royalty-free, transferable and sub-licensable, non-exclusive right to use, copy, modify, distribute, display, perform, create derivative works from and otherwise exploit all such feedback.
</template>

<script setup>
import { inject } from 'vue'

const i18n = inject('i18n')
</script>

<style scoped lang="stylus">

</style>
