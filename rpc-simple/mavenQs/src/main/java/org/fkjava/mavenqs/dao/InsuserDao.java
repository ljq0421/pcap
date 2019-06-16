package org.fkjava.mavenqs.dao;

import org.apache.ibatis.annotations.Mapper;
import org.fkjava.mavenqs.entity.Insuser;
import org.apache.ibatis.annotations.Param;

import java.util.List;
@Mapper
public interface InsuserDao {
    List<Insuser> getProject();
    List<Insuser> getVM(String project);
    List<Insuser> getPast(String pastshow,String displayname);
    List<Insuser> getPastAll(String displayname);
    List<Insuser> getName(String project);
    List<Insuser> getRule();
    List<Insuser> getRuleByRuleId(String ruleid);
    List<Insuser> getPastByRuleId(String ruleid);
    int makeRule(@Param("ruleinfo") String ruleinfo, @Param("insuser") Insuser insuser);
    int deleteRule(@Param("rulename") String rulename, @Param("ruleobject") String ruleobject,@Param("ruleinfo") String ruleinfo,@Param("rulestate") String rulestate,@Param("insuser") Insuser insuser);
}

