package org.fkjava.mavenqs.controller;
import com.alibaba.fastjson.JSON;
import org.fkjava.mavenqs.entity.Insuser;
import org.fkjava.mavenqs.entity.Response;
import org.fkjava.mavenqs.service.inter.InsuserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class InsuserController {
    @Autowired
    private InsuserService insuserService;

    @RequestMapping(value="/project")
    public Response getProject() {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getProject();
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toProject());
        }
        System.out.println(response);
        return response;
    }
    @RequestMapping(value="/project_name/{project}")
    public Response getName(@PathVariable String project) {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getName(project);
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toName());
        }
        return response;
    }
    @RequestMapping(value="/vm/{project}")
    public Response getVM(@PathVariable String project) {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getVM(project);
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toVM());
        }
        return response;
    }
    @RequestMapping(value="/pastby/{pastshow}/{displayname}")
    public Response getPast(@PathVariable String pastshow,@PathVariable String displayname) {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getPast(pastshow,displayname);
        System.out.println(pastshow+displayname);
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toPast(pastshow));
        }
        return response;
    }
    @RequestMapping(value="/past/{displayname}")
    public Response getPastAll(@PathVariable String displayname) {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getPastAll(displayname);
        System.out.println(displayname);
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toPastAll());
        }
        return response;
    }
    @RequestMapping(value="/rule_make/{ruleinfo}",method = RequestMethod.POST)
    public Response makeRule(@PathVariable String ruleinfo,@RequestBody String params) {
        Response response = new Response();
        Insuser insuser = JSON.parseObject(params, Insuser.class);
        System.out.println(ruleinfo);
        int result = insuserService.makeRule(ruleinfo,insuser);
        response.setDataV(result);
        System.out.println(result);
        return response;
    }
    @RequestMapping(value="/rule_delete/{rulename}/{ruleobject}/{ruleinfo}/{rulestate}",method = RequestMethod.POST)
    public Response deleteRule(@PathVariable String rulename,@PathVariable String ruleobject,@PathVariable String ruleinfo,@PathVariable String rulestate,@RequestBody String params) {
        Response response = new Response();
        Insuser insuser = JSON.parseObject(params, Insuser.class);
        int result = insuserService.deleteRule(rulename,ruleobject,ruleinfo,rulestate,insuser);
        response.setDataV(result);
        System.out.println(result);
        return response;
    }
    @RequestMapping(value="/rule_all")
    public Response getRule() {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getRule();
        System.out.println(insuser.get(0));
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toRule());
        }
        return response;
    }
    @RequestMapping(value="/rule_getbyid/{ruleid}")
    public Response getRuleById(@PathVariable String ruleid) {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getRuleByRuleId(ruleid);
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toRule());
        }
        return response;
    }
    @RequestMapping(value="/pastbyrule/{ruleid}")
    public Response getPastByRuleId(@PathVariable String ruleid) {
        Response response = new Response();
        List<Insuser> insuser = insuserService.getPastByRuleId(ruleid);
        for(int i=0;i<insuser.size();i++){
            response.setData(insuser.get(i).toPast(ruleid));
        }
        return response;
    }
}

