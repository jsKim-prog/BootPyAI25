package edu.mbcai.pybootai.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
    @GetMapping("/")
    public String home(){
        return "index"; //resources/templates/index.html
    } // http://localhost:80/ 반응하는 컨트롤러 -> 테스트 완료
}
