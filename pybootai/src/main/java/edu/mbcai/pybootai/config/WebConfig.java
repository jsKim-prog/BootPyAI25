package edu.mbcai.pybootai.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer { //컨트롤러 대행역할
    @Override
    public void addViewControllers(ViewControllerRegistry registry){
        registry.addViewController("/ai").setViewName("ai");
    }//html 페이지를 직접 요청할 수 있도록 뷰-컨트롤러 설정 추가
    // http://localhost:80/ai -> ai.html 실행
}
