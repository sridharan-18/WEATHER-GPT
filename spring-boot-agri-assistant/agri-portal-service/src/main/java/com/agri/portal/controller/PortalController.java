package com.agri.portal.controller;

import com.agri.portal.dto.QueryLog;
import com.agri.portal.service.PortalService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.Arrays;

/** MVC controller serving the Thymeleaf chat UI (port 8080). */
@Controller
public class PortalController {

    private final PortalService portalService;

    public PortalController(PortalService portalService) {
        this.portalService = portalService;
    }

    /** GET /  -> show the chat form + history of past questions. */
    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("log", portalService.findAll());
        return "index";
    }

    /** POST /ask  -> submit a query, fetch the advisory, store the log, re-render. */
    @PostMapping("/ask")
    public String ask(@ModelAttribute("log") QueryLog log, Model model) {
        String language = portalService.detectLanguage(log.getUserQuery());
        log.setDetectedLanguage(language);

        String[] result = portalService.callAdvisory(log.getUserQuery(), log.getDistrict());
        log.setAiResponse(result[0]);
        log.setSources(result[1].split(", "));

        portalService.save(log);
        model.addAttribute("log", portalService.findAll());
        return "redirect:/";
    }
}
