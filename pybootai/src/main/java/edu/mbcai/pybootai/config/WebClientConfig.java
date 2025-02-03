package edu.mbcai.pybootai.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {
    //WebClient를 구성하고 Bean으로 정의하여 애플리케이션에서 사용할 수 있도록 함
    //https://m.blog.naver.com/seek316/223337685249
    
    @Bean
    WebClient webClient(){
        return WebClient.builder().exchangeStrategies(ExchangeStrategies.builder()
                .codecs(confifurer->confifurer.defaultCodecs().maxInMemorySize(-1)).build())    //무제한 버퍼
                .baseUrl("http://localhost:8001")   //파이썬 ai 서버 주소 기재
                .build();   //업로드한 파일을 ai 서버에 전송하기 위해서 버퍼의 크기 제한을 제한 없이
    }
}
